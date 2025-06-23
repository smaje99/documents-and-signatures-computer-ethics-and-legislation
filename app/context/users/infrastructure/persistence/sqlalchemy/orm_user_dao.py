from typing import override

from app.context.shared.infrastructure.persistence.sqlalchemy import OrmDao
from app.context.users.domain import UserId
from app.context.users.infrastructure.persistence.sqlalchemy import OrmUserEntity


__all__ = ('OrmUserDao',)


class OrmUserDao(OrmDao[OrmUserEntity, UserId]):
  '''SQLAlchemy ORM DAO implementation for User entity.'''

  @override
  def __new__(cls, *args, **kwargs):
    instance = super().__new__(cls, *args, **kwargs)
    instance._entity = OrmUserEntity

    return instance

