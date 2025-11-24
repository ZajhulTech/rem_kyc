from typing import Dict, Type, TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.postgresql.postgres_base_repository import PostgresBaseRepository
from app.interfaces.database.unit_of_work import IUnitOfWork

T = TypeVar("T")

class PostgresUnitOfWork(IUnitOfWork, Generic[T]):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session: AsyncSession = None
        self._repositories: Dict[str, PostgresBaseRepository] = {}

    async def __aenter__(self):
        self.session = self.session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            await self.session.rollback()
        else:
            await self.session.commit()

        await self.session.close()

    def get_repository(self, model_cls: Type[T]) -> PostgresBaseRepository[T]:
        key = model_cls.__name__

        if key not in self._repositories:
            self._repositories[key] = PostgresBaseRepository[T](
                session=self.session,
                model_cls=model_cls
            )

        return self._repositories[key]

    async def commit(self):
        """Confirmar la transacción"""
        await self.session.commit()

    async def rollback(self):
        """Revertir la transacción"""
        await self.session.rollback()