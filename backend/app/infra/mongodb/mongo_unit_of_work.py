from typing import Dict, Type, TypeVar, Generic
from motor.motor_asyncio import AsyncIOMotorClient
from app.infra.mongodb.mongo_base_repository import MongoBaseRepository
from app.infra.mongodb.mongo_base_model import MongoBaseModel

T = TypeVar("T", bound=MongoBaseModel)

class MongoUnitOfWork(Generic[T]):
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self._repositories: Dict[str, MongoBaseRepository] = {}

    def get_repository(self, model_cls: Type[T]) -> MongoBaseRepository[T]:
        """
        Devuelve una instancia del repositorio correspondiente al modelo.
        Usa los atributos de `Settings` dentro del modelo.
        """
        key = model_cls.__name__

        if key not in self._repositories:
            # Validaciones de los campos obligatorios
            if not hasattr(model_cls, "Settings") or \
               not hasattr(model_cls.Settings, "db_name") or \
               not hasattr(model_cls.Settings, "collection_name"):
                raise ValueError(f"El modelo {model_cls.__name__} debe definir una clase Settings con 'db_name' y 'collection_name'.")

            db_name = model_cls.Settings.db_name
            collection_name = model_cls.Settings.collection_name

            self._repositories[key] = MongoBaseRepository[T](
                client=self.client,
                db_name=db_name,
                collection_name=collection_name,
                model_cls=model_cls
            )

        return self._repositories[key]

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"Excepción en UnitOfWork: {exc_val}")