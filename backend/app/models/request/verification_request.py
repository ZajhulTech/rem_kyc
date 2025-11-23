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
