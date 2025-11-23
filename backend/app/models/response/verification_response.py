from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class VerificationResponseDTO(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    phone: str
    country: str
    document_type: str
    document_number: str

    document_image_url: Optional[str] = None
    selfie_image_url: Optional[str] = None

    status: str
    risk_score: Optional[int] = None
    risk_level: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
