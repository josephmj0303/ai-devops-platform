from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing common CRUD operations.
    """

    def __init__(
        self,
        session: AsyncSession,
        model: type[ModelType],
    ):
        self.session = session
        self.model = model

    async def get_by_id(
        self,
        entity_id: UUID,
    ) -> ModelType | None:
        result = await self.session.execute(
            select(self.model).where(self.model.id == entity_id)
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        entity: ModelType,
    ) -> ModelType:
        self.session.add(entity)

        await self.session.commit()

        await self.session.refresh(entity)

        return entity

    async def delete(
        self,
        entity: ModelType,
    ) -> None:
        await self.session.delete(entity)

        await self.session.commit()
