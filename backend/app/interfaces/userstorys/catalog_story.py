# app/interfaces/userstorys/catalog_story.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.infra.api.response import Response

class ICatalogStory(ABC):
    @abstractmethod
    async def get_countries(self, code: Optional[str] = None) -> Response:
        pass
    
    @abstractmethod
    async def get_document_types(self, code: Optional[str] = None) -> Response:
        pass
    
    @abstractmethod
    async def get_risk_levels(self) -> Response:
        pass
    
    @abstractmethod
    async def get_verification_statuses(self) -> Response:
        pass