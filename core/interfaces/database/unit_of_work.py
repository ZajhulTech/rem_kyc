from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic

T = TypeVar("T")

class IUnitOfWork(ABC):
    @abstractmethod
    def get_repository(self, model_cls: Type[T]):
        pass
    
    @abstractmethod
    async def commit(self):
        """Confirmar la transacción"""
        pass
    
    @abstractmethod
    async def rollback(self):
        """Revertir la transacción"""
        pass