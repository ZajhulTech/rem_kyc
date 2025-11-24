from typing import List, Optional
from fastapi import HTTPException

from core.infra.api.response import Response
from core.interfaces.database.unit_of_work import IUnitOfWork
from core.interfaces.userstorys.catalog_story import ICatalogStory
from core.models.data_base.onbaording_models import (
    CountryCatalogModel, 
    DocumentTypeModel, 
    RiskLevelCatalogModel, 
    VerificationStatusModel
)
from core.models.response.catalog_response import (
    CountryResponseDTO,
    DocumentTypeResponseDTO, 
    RiskLevelResponseDTO,
    VerificationStatusResponseDTO,
    CatalogResponseDTO
)


class CatalogStory(ICatalogStory):
    def __init__(self, unit_of_work: IUnitOfWork):
        self._uow = unit_of_work

    async def get_countries(self, code: Optional[str] = None) -> Response:
        """
        Obtiene la lista de países.
        Si se proporciona un código, retorna solo ese país.
        """
        async with self._uow as uow:
            try:
                repo = uow.get_repository(CountryCatalogModel)
                
                filter_data = {}
                if code:
                    filter_data["code"] = code.upper()
                
                countries = await repo.find_all(filter_data)
                
                # Ordenar por nombre
                countries_sorted = sorted(countries, key=lambda x: x.name)
                
                countries_dto = [
                    CountryResponseDTO(
                        id=str(country.id),
                        code=country.code,
                        name=country.name,
                        calling_code=country.calling_code,
                        created_at=country.created_at,
                        updated_at=country.updated_at
                    )
                    for country in countries_sorted
                ]
                
                message = "Países obtenidos exitosamente"
                if code and countries_dto:
                    message = f"País con código '{code}' obtenido exitosamente"
                elif code and not countries_dto:
                    raise HTTPException(
                        status_code=404,
                        detail=f"País con código '{code}' no encontrado"
                    )
                
                return Response.with_data(
                    data=countries_dto,
                    message=message
                )
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error al obtener países: {str(e)}"
                )

    async def get_document_types(self, code: Optional[str] = None) -> Response:
        """
        Obtiene la lista de tipos de documento.
        Si se proporciona un código, retorna solo ese tipo.
        """
        async with self._uow as uow:
            try:
                repo = uow.get_repository(DocumentTypeModel)
                
                filter_data = {}
                if code:
                    filter_data["code"] = code.upper()
                
                document_types = await repo.find_all(filter_data)
                
                document_types_dto = [
                    DocumentTypeResponseDTO(
                        id=str(doc_type.id),
                        code=doc_type.code,
                        description=doc_type.description
                    )
                    for doc_type in document_types
                ]
                
                message = "Tipos de documento obtenidos exitosamente"
                if code and document_types_dto:
                    message = f"Tipo de documento con código '{code}' obtenido exitosamente"
                elif code and not document_types_dto:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Tipo de documento con código '{code}' no encontrado"
                    )
                
                return Response.with_data(
                    data=document_types_dto,
                    message=message
                )
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error al obtener tipos de documento: {str(e)}"
                )

    async def get_risk_levels(self) -> Response:
        """
        Obtiene la lista de niveles de riesgo.
        """
        async with self._uow as uow:
            try:
                repo = uow.get_repository(RiskLevelCatalogModel)
                risk_levels = await repo.find_all({})
                
                risk_levels_dto = [
                    RiskLevelResponseDTO(
                        id=str(risk_level.id),
                        code=risk_level.code,
                        description=risk_level.description
                    )
                    for risk_level in risk_levels
                ]
                
                return Response.with_data(
                    data=risk_levels_dto,
                    message="Niveles de riesgo obtenidos exitosamente"
                )
                
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error al obtener niveles de riesgo: {str(e)}"
                )

    async def get_verification_statuses(self) -> Response:
        """
        Obtiene la lista de estados de verificación.
        """
        async with self._uow as uow:
            try:
                repo = uow.get_repository(VerificationStatusModel)
                statuses = await repo.find_all({})
                
                statuses_dto = [
                    VerificationStatusResponseDTO(
                        id=str(status.id),
                        code=status.code,
                        description=status.description
                    )
                    for status in statuses
                ]
                
                return Response.with_data(
                    data=statuses_dto,
                    message="Estados de verificación obtenidos exitosamente"
                )
                
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error al obtener estados de verificación: {str(e)}"
                )

    async def get_all_catalogs(self) -> Response:
        """
        Obtiene todos los catálogos en una sola respuesta.
        """
        async with self._uow as uow:
            try:
                countries = await self.get_countries()
                document_types = await self.get_document_types()
                risk_levels = await self.get_risk_levels()
                verification_statuses = await self.get_verification_statuses()
                
                all_catalogs = CatalogResponseDTO(
                    countries=countries.data,
                    document_types=document_types.data,
                    risk_levels=risk_levels.data,
                    verification_statuses=verification_statuses.data
                )
                
                return Response.with_data(
                    data=all_catalogs,
                    message="Todos los catálogos obtenidos exitosamente"
                )
                
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error al obtener catálogos: {str(e)}"
                )