from typing import Any, Dict, List, Optional, Type, TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import DeclarativeMeta

T = TypeVar("T")

class PostgresBaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model_cls: Type[T]):
        self.session = session
        self.model = model_cls

    async def find_by_id(self, id: Any) -> Optional[T]:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def find(self, filter: Dict[str, Any]) -> Optional[T]:
        query = select(self.model).filter_by(**filter)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def find_all(self, filter: Dict[str, Any]) -> List[T]:
        query = select(self.model).filter_by(**filter)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def insert(self, data: T) -> Any:
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def update(self, id: Any, data: Dict[str, Any]) -> int:
        query = (
            self.model.__table__
            .update()
            .where(self.model.id == id)
            .values(**data)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount

    async def delete(self, id: Any) -> int:
        query = self.model.__table__.delete().where(self.model.id == id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount

    async def count(self, filter: Dict[str, Any]) -> int:
        query = select(func.count()).select_from(self.model).filter_by(**filter)
        result = await self.session.execute(query)
        return result.scalar()

    async def paginate(
        self,
        filter: Dict[str, Any],
        page: int = 1,
        page_size: int = 10,
        sort: Optional[List[Any]] = None
    ) -> Dict[str, Any]:

        offset = (page - 1) * page_size

        # Base query
        query = select(self.model).filter_by(**filter)

        # Sorting
        if sort:
            query = query.order_by(*sort)

        # Execute paged query
        result = await self.session.execute(
            query.offset(offset).limit(page_size)
        )
        items = result.scalars().all()

        # Count total items
        total_query = select(func.count()).select_from(self.model).filter_by(**filter)
        total_result = await self.session.execute(total_query)
        total = total_result.scalar()

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }
