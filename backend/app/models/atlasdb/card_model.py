from pydantic import BaseModel
from typing import Optional
from datetime import date

class CardModel(BaseModel):
    card_number: str
    level: int
    points: float
    expiration_date: date
    is_enabled: bool
