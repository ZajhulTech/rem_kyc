from typing import TypeVar, Generic, Optional, List, Dict, Any, Type
from bson import ObjectId
from core.interfaces.database.base_repository import IBaseRepository
from core.infra.mongodb.mongo_base_model import MongoBaseModel
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

T = TypeVar("T", bound=MongoBaseModel)

class MongoBaseRepository(IBaseRepository[T], Generic[T]):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        db_name: str,
        collection_name: str,
        model_cls: Type[T]
    ):
        """
        Inicializa el repositorio de MongoDB (asíncrono).
        """
        self.db = client[db_name]
        self.collection: AsyncIOMotorCollection = self.db[collection_name]
        self.model_cls = model_cls

    async def find_by_id(self, id: str) -> Optional[T]:
        try:
            document = await self.collection.find_one({"_id": ObjectId(id)})
            return self._to_entity(document) if document else None
        except Exception as e:
            print(f"Error al buscar por ID: {e}")
            return None

    async def find(self, filter: Dict[str, Any]) -> Optional[T]:
        document = await self.collection.find_one(filter)
        return self._to_entity(document) if document else None

    async def find_all(self, filter: Optional[Dict[str, Any]] = None) -> List[T]:
        filter = filter or {}
        cursor = self.collection.find(filter)
        return [self._to_entity(doc) async for doc in cursor]

    async def insert(self, data: T) -> str:
        data_dict = data.model_dump(by_alias=True, exclude_none=True)
        result = await self.collection.insert_one(data_dict)
        return str(result.inserted_id)

    async def update(self, id: str, data: Dict[str, Any]) -> int:
        result = await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )
        return result.modified_count

    async def delete(self, id: str) -> int:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count

    async def count(self, filter: Dict[str, Any]) -> int:
        filter = filter or {}
        return await self.collection.count_documents(filter)
    
    async def paginate(self, filter, page=1, page_size=10, sort=None):
        skip = (page - 1) * page_size
        
        cursor = self.collection.find(filter)

        if sort:
            cursor = cursor.sort(sort)

        items = await cursor.skip(skip).limit(page_size).to_list(length=page_size)
        total = await self.collection.count_documents(filter)

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }

    def _to_entity(self, document: Dict[str, Any]) -> T:
        document["id"] = str(document["_id"])
        return self.model_cls.model_validate(document)