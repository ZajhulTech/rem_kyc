from abc import ABC, abstractmethod
from typing import List
from app.models.response.customer_response import CustomerResponse
from app.infra.api.response import Response

class ICustomerStory(ABC):
    @abstractmethod
    async def get_customer(self) -> Response[List[CustomerResponse]]:
        pass