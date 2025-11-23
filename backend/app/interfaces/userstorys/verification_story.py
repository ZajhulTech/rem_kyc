from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.response.verification_response import VerificationResponseDTO
from app.infra.api.response import Response


class IVerificationStory(ABC):

    @abstractmethod
    async def get_verifications_paginated(
        self,
        page: int,
        page_size: int,
        status: Optional[str] = None
    ) -> Response[List[VerificationResponseDTO]]:
        pass
