from pydantic import Field, EmailStr
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.models.atlasdb.card_model import CardModel
from pydantic import BaseModel

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):  # <-- aquí acepta info opcional
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema):
        return {
            "type": "string",
            "pattern": "^[a-fA-F0-9]{24}$",
            "title": "ObjectId",
            "description": "MongoDB ObjectId represented as a 24-character hex string"
        }

class CustomerModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    whatsapp_number: str
    email: EmailStr  # Valida automáticamente emails
    name: str
    last_name: str
    birthdate: datetime
    gender: str
    status: str
    brand: str
    card: Optional[List[CardModel]] = []
    created: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True,
        "json_encoders": {
            PyObjectId: str,
            ObjectId: str,
        },
        "populate_by_alias": True,
        "validate_default": True,
        "from_attributes": True,
    }

    class Settings: # type: ignore
        db_name = "chatbot_lealtad"
        collection_name = "customers"
