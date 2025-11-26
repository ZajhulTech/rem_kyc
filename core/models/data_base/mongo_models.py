from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from core.models.rule_engine import RuleType, RiskLevel


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
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

class VerificationLogModel(BaseModel):

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
            RuleType: lambda v: v.value
        },
        use_enum_values=True,  
        str_strip_whitespace=True,
        validate_assignment=True
    )
    
    id: Optional[PyObjectId] = Field(None, alias="_id")
    request_id: str
    score: int
    risk_level: RiskLevel
    rules_triggered: List[RuleType]
    rules_detail: Dict[RuleType, Dict[str, Any]]
    engine_version: str = "1.0.0"
    processed_at: datetime
    processing_time_ms: int
    created: datetime = Field(default_factory=datetime.now)
    
    class Settings:
        db_name = "kyc"
        collection_name = "verification_logs"