from fastapi import HTTPException
from typing import Optional

from app.infra.api.response import Response
from app.interfaces.database.unit_of_work import IUnitOfWork
from app.interfaces.userstorys.verification_story import IVerificationStory
from app.models.response.verification_response import VerificationResponseDTO
from app.models.onboarding.verification_request_model import VerificationRequestModel
from app.infra.postgresql.postgres_base_repository import PostgresBaseRepository


class VerificationStory(IVerificationStory):
    def __init__(self, unit_of_work: IUnitOfWork):
        self._uow = unit_of_work

    async def get_verifications_paginated(
        self,
        page: int = 1,
        page_size: int = 10,
        status: Optional[str] = None,
        sort: Optional[list] = None
    ) -> Response:

        filter_data = {}
        if status:
            filter_data["status"] = status

        async with self._uow as uow:
            repo: PostgresBaseRepository[VerificationRequestModel] = uow.get_repository(VerificationRequestModel)

            try:
                paginated = await repo.paginate(
                    filter=filter_data,
                    page=page,
                    page_size=page_size,
                    sort=sort
                )

                # Map ORM → DTO
                paginated["items"] = [
                    VerificationStory.to_verification_response(item)
                    for item in paginated["items"]
                ]

            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error al obtener las verificaciones paginadas: {str(e)}"
                )

        return Response.with_data(paginated)

    # -------------------------------------------------------------------
    # Mapping ORM → DTO
    # -------------------------------------------------------------------
    @staticmethod
    def to_verification_response(entity: VerificationRequestModel) -> VerificationResponseDTO:
        return VerificationResponseDTO(
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
