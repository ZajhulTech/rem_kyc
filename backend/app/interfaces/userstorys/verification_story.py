from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.response.verification_response import VerificationResponseDTO
from app.infra.api.response import Response
from app.models.request.verification_request import VerificationCreateRequestDTO


class IVerificationStory(ABC):

    @abstractmethod
    async def get_verifications_paginated(
        self,
        page: int,
        page_size: int,
        filter: Optional[str] = None
    ) -> Response[List[VerificationResponseDTO]]:
        pass

    @abstractmethod    
    async def get_verification_by_id(
        self,
        verification_id: str
    ) -> Response:
        pass

    @abstractmethod
    async def create_verification(
        self,
        verification_data: VerificationCreateRequestDTO
    ) -> Response:
        pass