from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CountryResponseDTO(BaseModel):
    id: str
    code: str
    name: str
    calling_code: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class DocumentTypeResponseDTO(BaseModel):
    id: str
    code: str
    description: str

class RiskLevelResponseDTO(BaseModel):
    id: str
    code: str
    description: str

class VerificationStatusResponseDTO(BaseModel):
    id: str
    code: str
    description: str

class CatalogResponseDTO(BaseModel):
    countries: List[CountryResponseDTO]
    document_types: List[DocumentTypeResponseDTO]
    risk_levels: List[RiskLevelResponseDTO]
    verification_statuses: List[VerificationStatusResponseDTO]