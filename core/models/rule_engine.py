from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RuleType(str, Enum):
    EMAIL_DOMAIN_RISK = "EMAIL_DOMAIN_RISK"
    COUNTRY_RESTRICTED = "COUNTRY_RESTRICTED"
    DOCUMENT_LENGTH_INVALID = "DOCUMENT_LENGTH_INVALID"

class RuleConfig(BaseModel):
    risky_domains: List[str] = ["tempmail.com", "riskmail.com", "fake.com"]
    restricted_countries: List[str] = ["22222222-2222-2222-2222-222222222222","aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"]  # UUIDs de países
    min_document_length: int = 8

class RuleResult(BaseModel):
    rule_type: RuleType
    triggered: bool
    score_penalty: int
    details: Dict[str, Any]

class RiskAssessmentResult(BaseModel):
    score: int
    risk_level: RiskLevel
    rules_triggered: List[RuleType]
    rules_detail: Dict[RuleType, Dict[str, Any]]
    processing_time_ms: int