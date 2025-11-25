from abc import ABC, abstractmethod
from typing import Optional
from core.models.rule_engine import RiskAssessmentResult, RuleConfig


class IRuleEngineStory(ABC):
    @abstractmethod
    async def assess_risk(self, verification_data, config: Optional[RuleConfig] = None) -> RiskAssessmentResult:
        pass
    
    @abstractmethod
    async def process_pending_verifications(self, batch_size: int = 100) -> dict:
        pass