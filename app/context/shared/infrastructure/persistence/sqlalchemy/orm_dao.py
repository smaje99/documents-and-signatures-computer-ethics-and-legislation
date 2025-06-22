from abc import ABCMeta
from typing import override
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect
from sqlalchemy.sql.expression import BinaryExpression, select

from app.context.shared.domain import BaseDAO
from app.context.shared.domain.errors import DaoError
from app.database import Base
from app.database.postgres import PostgresDatabase


__all__ = ('OrmDao',)


class OrmDao[EntityBase: Base, EntityId: UUID | str](
  BaseDAO[EntityBase, EntityId],
  metaclass=ABCMeta
):
  '''Abstract SQLAlchemy ORM DAO.'''

  def __init__(self, database: PostgresDatabase):
    '''Abstract SQLAlchemy ORM DAO constructor.

    Args:
        database (PostgresDatabase): Database session.
    '''
    self._entity: type[EntityBase]
    self._database = database

  async def __upsert(self, entity: EntityBase, session: AsyncSession) -> EntityBase:
    '''Save or update an entity.

    Args:
        entity (Entity): Entity to upsert.
        session (AsyncSession): Database session.

    Returns:
        Entity: Upserted entity.
    '''
    session.add(entity)
    await session.commit()
    await session.refresh(entity)

    return entity

  @override
  async def save(self, entity: EntityBase):
    async with self._database.session() as session:
      try:
        return await self.__upsert(entity, session)
      except SQLAlchemyError as error:
        raise DaoError.save_operation_failed() from error

  @override
  async def update(self, entity: EntityBase) -> EntityBase:
    async with self._database.session() as session:
      try:
        return await self.__upsert(entity, session)
      except SQLAlchemyError as error:
        raise DaoError.update_operation_failed() from error

  @override
  async def search(self, entity_id: EntityId) -> EntityBase | None:
    async with self._database.session() as session:
      try:
        return await session.get(self._entity, entity_id)
      except SQLAlchemyError as error:
        raise DaoError.retrieve_operation_failed() from error

  @override
  async def filter(self, *expressions: BinaryExpression) -> list[EntityBase]:
    async with self._database.session() as session:
      try:
        query = select(self._entity)

        if expressions:
          query = query.where(*expressions)

        result = await session.scalars(query)
        return list(result.all())
      except SQLAlchemyError as error:
        raise DaoError.retrieve_operation_failed() from error

  @override
  async def delete(self, entity: EntityBase) -> EntityBase:
    async with self._database.session() as session:
      try:
        await session.delete(entity)
        await session.commit()
      except SQLAlchemyError as error:
        raise DaoError.delete_operation_failed() from error

      return entity

  @override
  async def exists(self, entity_id: EntityId) -> bool:
    async with self._database.session() as session:
      try:
        entity_pk = inspect(self._entity).primary_key[0]
        sub_query = select(1).where(entity_pk == entity_id)
        query = select(sub_query.exists())
        result = await session.scalar(query)

        return bool(result)
      except SQLAlchemyError as error:
        raise DaoError.retrieve_operation_failed() from error
