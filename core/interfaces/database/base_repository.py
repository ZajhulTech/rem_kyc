from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

T = TypeVar("T")

class IBaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def find_by_id(self, id: Any) -> Optional[T]: ...
    
    @abstractmethod
    async def find(self, filter: Dict[str, Any]) -> Optional[T]: ...
    
    @abstractmethod
    async def find_all(self, filter: Dict[str, Any]) -> List[T]: ...
    
    @abstractmethod
    async def insert(self, data: T) -> Any: ...
    
    @abstractmethod
    async def update(self, id: Any, data: Dict[str, Any]) -> int: ...
    
    @abstractmethod
    async def delete(self, id: Any) -> int: ...
    
    @abstractmethod
    async def count(self, filter: Dict[str, Any]) -> int: ...

    @abstractmethod
    async def paginate(
        self, 
        filter: Dict[str, Any], 
        page: int = 1, 
        page_size: int = 10,
        sort: Optional[List[tuple]] = None
    ) -> Dict[str, Any]: ...

