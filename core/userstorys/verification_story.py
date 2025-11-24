from datetime import datetime
import uuid
from fastapi import HTTPException
from typing import Optional

from core.infra.api.response import Response
from core.interfaces.database.unit_of_work import IUnitOfWork
from core.interfaces.userstorys.verification_story import IVerificationStory
from core.models.response.verification_response import VerificationResponseDTO, VerificationDetailResponseDTO
from core.models.request.verification_request import VerificationCreateRequestDTO, VerificationStatusUpdateRequestDTO
from core.models.data_base.onbaording_models import VerificationStatusModel,DocumentTypeModel,RiskLevelCatalogModel,CountryCatalogModel,VerificationRequestModel,VerificationRequestViewModel
from core.infra.postgresql.postgres_base_repository import PostgresBaseRepository


class VerificationStory(IVerificationStory):
    def __init__(self, unit_of_work: IUnitOfWork):
        self._uow = unit_of_work

    async def get_verifications_paginated(
        self,
        page: int = 1,
        page_size: int = 10,
        filter: Optional[str] = None,
        sort: Optional[list] = None
    ) -> Response:
        """
        Obtiene el listado paginado de verificaciones con filtro unificado.
        
        Args:
            page: Número de página
            page_size: Tamaño de página
            filter: Texto para buscar en estado o nombre (búsqueda parcial)
            sort: Campos para ordenar
        """

        filter_data = {}
       
        if filter:
            filter_data["status"] = filter
            filter_data["full_name"] = filter

        async with self._uow as uow:
            repo: PostgresBaseRepository[VerificationRequestViewModel] = uow.get_repository(VerificationRequestViewModel)

            paginated = await repo.find_filter_paginated(
                filter=filter_data,
                page=page,
                page_size=page_size,
                sort=["-created_at"]
            )

            # Map ORM → DTO
            paginated["items"] = [
                VerificationStory.to_verification_response(item)
                for item in paginated["items"]
            ]

        return Response.with_data(paginated)


    async def get_verification_by_id(
        self,
        verification_id: str
    ) -> Response:
        """
        Obtiene el detalle de una verificación por ID.
        """
        async with self._uow as uow:
            repo: PostgresBaseRepository[VerificationRequestViewModel] = uow.get_repository(VerificationRequestViewModel)

            entity = await repo.find_by_id(verification_id)

            if not entity:
                raise HTTPException(
                    status_code=404,
                    detail=f"No se encontró la verificación con ID {verification_id}"
                )

            detail = VerificationStory.to_verification_detail_response(entity)

        return Response.with_data(detail)


    async def create_verification(
        self,
        verification_data: VerificationCreateRequestDTO
    ) -> Response:
        """
        Crea una nueva solicitud de verificación sin calcular riesgo inicial.
        """
        async with self._uow as uow:
      
            # 1. Generar ID único y timestamp
            verification_id = str(uuid.uuid4())
            current_time = datetime.utcnow()
            
            # 2. Buscar IDs de las tablas de referencia por CÓDIGO
            status_repo = uow.get_repository(VerificationStatusModel)
            document_type_repo = uow.get_repository(DocumentTypeModel)
            risk_level_repo = uow.get_repository(RiskLevelCatalogModel)
            country_repo = uow.get_repository(CountryCatalogModel)
            
            # Obtener status "pendiente" por código
            pending_status = await status_repo.find_one_by({"code": "pending"})
            if not pending_status:
                raise HTTPException(
                    status_code=500,
                    detail="No se encontró el estado 'pendiente' en el sistema"
                )
            
            # Obtener tipo de documento por código
            document_type = await document_type_repo.find_one_by({"code": verification_data.document_type_code})
            if not document_type:
                raise HTTPException(
                    status_code=400,
                    detail=f"Tipo de documento '{verification_data.document_type_code}' no válido"
                )
            
            # Obtener país por código
            country = await country_repo.find_one_by({"code": verification_data.country_code})
            if not country:
                raise HTTPException(
                    status_code=400,
                    detail=f"País con código '{verification_data.country_code}' no encontrado"
                )
            
            # Obtener risk_level "por determinar" (n/c)
            pending_risk_level = await risk_level_repo.find_one_by({"code": "n/c"})
            if not pending_risk_level:
                raise HTTPException(
                    status_code=500,
                    detail="No se encontró el nivel de riesgo 'por determinar' en el sistema"
                )
            
            # 3. Validar formato de teléfono (opcional, puede usar el calling_code del país)
            # Podrías agregar validación aquí usando country.calling_code
            
            # 4. Crear la entidad
            verification_repo = uow.get_repository(VerificationRequestModel)
            
            new_verification = VerificationRequestModel(
                id=verification_id,
                full_name=verification_data.full_name,
                email=verification_data.email,
                phone=verification_data.phone,
                country_id=country.id,  # ← ID del país
                document_type_id=document_type.id,  # ← ID del tipo de documento
                document_number=verification_data.document_number,
                document_image_url=verification_data.document_image_url,
                selfie_image_url=verification_data.selfie_image_url,
                status_id=pending_status.id,
                risk_score=None,  # NULL inicialmente
                risk_level_id=pending_risk_level.id,  # "por determinar"
                created_at=current_time,
                updated_at=current_time
            )
            
            await verification_repo.create(new_verification)
            await uow.commit()
            
            # 5. Obtener la entidad creada para la respuesta
            view_repo = uow.get_repository(VerificationRequestViewModel)
            created_entity = await view_repo.find_by_id(verification_id)
            
            if not created_entity:
                raise HTTPException(
                    status_code=500,
                    detail="Error al recuperar la verificación creada"
                )
            
            # 6. Convertir a DTO de respuesta
            response_data = VerificationStory.to_verification_response(created_entity)
                
        return Response.with_data(
            data=response_data,
            message="Solicitud de verificación creada exitosamente. El análisis de riesgo se procesará en segundo plano."
        )


    async def update_verification_status(
            self,
            status_update_data: VerificationStatusUpdateRequestDTO
        ) -> Response:
        """
        Actualiza el estado de una solicitud de verificación.
        """
        verification_id = str(status_update_data.verification_id)
        new_status_code = status_update_data.status_code
        
        async with self._uow as uow:

            # 1. Buscar la verificación existente en la VISTA (ya incluye el estado)
            view_repo = uow.get_repository(VerificationRequestViewModel)
            existing_verification_view = await view_repo.find_by_id(verification_id)
            
            if not existing_verification_view:
                raise HTTPException(
                    status_code=404,
                    detail=f"No se encontró la verificación con ID {verification_id}"
                )

            # 2. Buscar el nuevo estado por código
            status_repo = uow.get_repository(VerificationStatusModel)
            new_status = await status_repo.find_one_by({"code": new_status_code})
            
            if not new_status:
                raise HTTPException(
                    status_code=400,
                    detail=f"Estado '{new_status_code}' no válido"
                )

            # 3. Obtener el estado actual desde la VISTA - CORREGIDO
            current_status_code = existing_verification_view.status.lower()  # Convertir a minúsculas para comparar

            # 3. Validar transición de estado
            valid_transitions = {
                "pending": ["approved", "rejected", "requires_information"],
                "requires_information": ["pending", "approved", "rejected"],
                "approved": ["rejected"],
                "rejected": ["pending"]
            }
            
            if (current_status_code in valid_transitions and 
                new_status_code not in valid_transitions[current_status_code]):
                raise HTTPException(
                    status_code=400,
                    detail=f"No se puede cambiar el estado de '{current_status_code}' a '{new_status_code}'"
                )

            # 4. Actualizar el estado y timestamp
            current_time = datetime.utcnow()
            
            update_data = {
                "status_id": new_status.id,
                "updated_at": current_time
            }

            # 5. Ejecutar la actualización en el modelo principal
            verification_repo = uow.get_repository(VerificationRequestModel)
            await verification_repo.update(verification_id, update_data)
            await uow.commit()

            # 6. Obtener la entidad actualizada para la respuesta
            updated_entity = await view_repo.find_by_id(verification_id)
            
            if not updated_entity:
                raise HTTPException(
                    status_code=500,
                    detail="Error al recuperar la verificación actualizada"
                )

            # 7. Convertir a DTO de respuesta
            response_data = self.to_verification_response(updated_entity)

        return Response.with_data(
            data=response_data,
            message=f"Estado de la verificación actualizado exitosamente a '{new_status_code}'"
        )

    # -------------------------------------------------------------------
    # Mapping ORM → DTO
    # -------------------------------------------------------------------
    @staticmethod
    def to_verification_response(entity: VerificationRequestViewModel) -> VerificationResponseDTO:
        return VerificationResponseDTO(
            id=str(entity.id),
            full_name=entity.full_name,
            email=entity.email,
            country=entity.country,        
            status=entity.status,
            created_at=entity.created_at

        )

    @staticmethod
    def to_verification_detail_response(entity: VerificationRequestViewModel) -> VerificationDetailResponseDTO:
        return VerificationDetailResponseDTO(
            id=str(entity.id),
            full_name=entity.full_name,
            email=entity.email,
            phone=entity.phone,
            country=entity.country,
            document_type=entity.document_type,
            document_number=entity.document_number,
            document_image_url=entity.document_image_url,
            selfie_image_url=entity.selfie_image_url,
            status=entity.status,
            risk_score=entity.risk_score,
            risk_level=entity.risk_level,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
