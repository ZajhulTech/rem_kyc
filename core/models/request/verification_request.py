from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Optional

class VerificationRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    country: str
    document_type: str
    document_number: str

    document_image_url: Optional[str] = None
    selfie_image_url: Optional[str] = None

    class Config:
        from_attributes = True

class VerificationCreateRequestDTO(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    country_code: str
    document_type_code: str
    document_number: str
    document_image_url: Optional[str] = None
    selfie_image_url: Optional[str] = None
    
    class Config:
        from_attributes = True


class VerificationStatusUpdateRequestDTO(BaseModel):
    verification_id: UUID
    status_code: str  # "approved", "rejected", "requires_information", etc.