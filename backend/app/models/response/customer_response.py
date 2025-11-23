from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from app.models.response.card_response import CardResponse  # Asegúrate que esto exista

class CustomerResponse(BaseModel):
    id: str
    whatsapp_number: str
    email: EmailStr
    name: str
    last_name: str
    birthdate: datetime
    gender: str
    status: str
    brand: str
    card: Optional[List[CardResponse]] = Field(default_factory=list)
    created: datetime