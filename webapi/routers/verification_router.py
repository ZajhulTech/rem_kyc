from typing import Optional
from core.models.request.verification_request import VerificationCreateRequestDTO, VerificationStatusUpdateRequestDTO
from fastapi import APIRouter, Depends, Query
from uuid import UUID
from core.userstorys.verification_story import VerificationStory
from core.interfaces.userstorys.verification_story import IVerificationStory
from core.infra.api.response import Response
from core.models.response.verification_response import VerificationResponseDTO, VerificationDetailResponseDTO
from webapi.dependencies.postgres_dependencies import get_postgres_unit_of_work

router = APIRouter()
base = "/api/v1/verification"
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
    filter: Optional[str] = Query(None),
    user_story: IVerificationStory = Depends(get_user_story)
):
    """
    Obtener solicitudes de verificación paginadas
    """
    return await user_story.get_verifications_paginated(
        page=page,
        page_size=page_size,
        filter=filter
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

@router.put(
    base + "/status",
    response_model=Response,
    tags=[Tag]
)
async def update_verification_status_endpoint(
    status_data: VerificationStatusUpdateRequestDTO,
    user_story: VerificationStory = Depends(get_user_story)
):
    """
    Actualiza el estado de una solicitud de verificación.
    """
    return await user_story.update_verification_status(status_data)