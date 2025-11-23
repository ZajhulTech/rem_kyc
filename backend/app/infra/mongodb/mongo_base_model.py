#  Pydantic v2
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from app.models.atlasdb.customer_model import PyObjectId

class MongoBaseModel(BaseModel):
    """
    Modelo base para documentos MongoDB con ObjectId.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str,
        }
    }

    class Settings:
        db_name = ""
        collection_name = ""