from typing import Any, Dict, List, Optional, Type, TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
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

    async def find_one_by(self, filter: Dict[str, Any]) -> Optional[T]:
        query = select(self.model).filter_by(**filter)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def find_all(self, filter: Dict[str, Any]) -> List[T]:
        query = select(self.model).filter_by(**filter)
        result = await self.session.execute(query)
        return result.scalars().all()


    async def create(self, data: T) -> Any:
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

    async def find_filter_paginated(
        self,
        filter: Dict[str, Any],
        page: int = 1,
        page_size: int = 10,
        sort: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        """
        Función genérica para paginar cualquier modelo (tabla o vista),
        usando filter dict y sort opcional.
        
        Args:
            filter: Diccionario con filtros
                - Si hay múltiples campos con el mismo valor: búsqueda OR
                - Campos individuales: búsqueda exacta
            page: Número de página
            page_size: Tamaño de página
            sort: Lista de campos para ordenar
        """

        offset = (page - 1) * page_size

        query = select(self.model)
        count_query = select(func.count()).select_from(self.model)

        # Aplicar filtros
        if filter:
            # Verificar si hay múltiples filtros con el mismo valor (búsqueda OR)
            filter_values = list(filter.values())
            if len(filter) > 1 and len(set(filter_values)) == 1:
                # Múltiples campos con el mismo valor → búsqueda OR
                search_value = f"%{filter_values[0]}%"
                conditions = []
                
                for key in filter.keys():
                    field = getattr(self.model, key)
                    conditions.append(field.ilike(search_value))
                
                # Aplicar condición OR
                query = query.where(or_(*conditions))
                count_query = count_query.where(or_(*conditions))
            else:
                # Filtros individuales → búsqueda exacta
                for key, value in filter.items():
                    field = getattr(self.model, key)
                    query = query.where(field == value)
                    count_query = count_query.where(field == value)

        # Sorting mejorado
        if sort:
            order_by_clauses = []
            for sort_item in sort:
                if isinstance(sort_item, str):
                    # Si es string, verificar si es descendente
                    if sort_item.startswith('-'):
                        field_name = sort_item[1:]  # Remover el '-'
                        field = getattr(self.model, field_name)
                        order_by_clauses.append(field.desc())
                    else:
                        # Orden ascendente por defecto
                        field = getattr(self.model, sort_item)
                        order_by_clauses.append(field.asc())
                else:
                    # Si ya es una expresión SQLAlchemy (asc(), desc())
                    order_by_clauses.append(sort_item)
            
            query = query.order_by(*order_by_clauses)

        # Ejecutar query paginada
        result = await self.session.execute(query.offset(offset).limit(page_size))
        items = result.scalars().all()

        # Contar total de items
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }