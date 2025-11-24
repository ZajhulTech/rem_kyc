from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class VerificationResponseDTO(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    country: str
    status: str
    created_at: datetime
   
    class Config:
        from_attributes = True


class VerificationDetailResponseDTO(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    country: str
    document_type: Optional[str] = None
    document_number: Optional[str] = None

    document_image_url: Optional[str] = None
    selfie_image_url: Optional[str] = None

    status: str
    risk_score: Optional[int] = None
    risk_level: Optional[str] = None

    created_at: datetime
    updated_at: Optional[datetime] = None 

    class Config:
        from_attributes = True
