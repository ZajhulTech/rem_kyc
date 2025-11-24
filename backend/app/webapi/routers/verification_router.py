from typing import Optional
from app.models.request.verification_request import VerificationCreateRequestDTO
from fastapi import APIRouter, Depends, Query
from uuid import UUID
from app.userstorys.verification_story import VerificationStory
from app.interfaces.userstorys.verification_story import IVerificationStory
from app.infra.api.response import Response
from app.models.response.verification_response import VerificationResponseDTO, VerificationDetailResponseDTO
from app.webapi.dependencies.postgres_dependencies import get_postgres_unit_of_work

router = APIRouter()
base = "/verification"
Tag = "Verification Requests"


# Dependency injector
def get_user_story(uow=Depends(get_postgres_unit_of_work)) -> IVerificationStory:
    return VerificationStory(uow)  # type: ignore


# GET paginated verification requests
@router.get(
    base,
    response_model=Response,
    tags=[Tag]
)
async def get_verifications(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    user_story: IVerificationStory = Depends(get_user_story)
):
    """
    Obtener solicitudes de verificación paginadas
    """
    return await user_story.get_verifications_paginated(
        page=page,
        page_size=page_size,
        status=status
    )


@router.get(
        (base+"/detail"), 
        response_model=Response[VerificationDetailResponseDTO],
        tags=[Tag]
)
async def get_verification_detail(
    id: UUID = Query(None),
    user_story: VerificationStory = Depends(get_user_story)
    ):

    return await user_story.get_verification_by_id(id)

@router.post(
    base, 
    response_model=Response,
    status_code=201,
    tags=[Tag]
)
async def create_verification_endpoint(
    verification_data: VerificationCreateRequestDTO,
    user_story: VerificationStory = Depends(get_user_story)
    ):
    """
    Crea una nueva solicitud de verificación KYC.
    """
    return await user_story.create_verification(verification_data)