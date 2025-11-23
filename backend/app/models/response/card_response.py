from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class CardResponse(BaseModel):
    card_number: str
    level: int
    points: float
    expiration_date: date
    is_enabled: bool