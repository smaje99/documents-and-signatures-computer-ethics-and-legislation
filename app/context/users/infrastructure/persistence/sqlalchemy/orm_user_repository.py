from typing import override

from app.context.users.domain import User, UserId, UserRepository, UserSaveDto
from app.context.users.infrastructure.persistence.sqlalchemy import (
  OrmUserDao,
  OrmUserEntity,
)
from app.core.security.pwd import get_password_hash


__all__ = ('OrmUserRepository',)


class OrmUserRepository(UserRepository):
  '''SQLAlchemy ORM implementation of UserRepository.'''

  def __init__(self, dao: OrmUserDao):
    '''Initialize OrmUserRepository.

    Args:
        dao (OrmUserDao): Data Access Object for user.
    '''
    self.__dao = dao

  @override
  async def save(self, user_in: UserSaveDto) -> User:
    obj_in_user = user_in.model_dump()
    obj_in_user['hash_password'] = get_password_hash(obj_in_user.pop('password', None))

    orm_user = OrmUserEntity(**obj_in_user)
    db_user = await self.__dao.save(orm_user)

    return User.model_validate(db_user)

  @override
  async def contains(self, user_id: UserId) -> bool:
    return await self.__dao.exists(user_id)

  @override
  async def contains_email(self, email: str) -> bool:
    users = await self.__dao.filter(OrmUserEntity.email.like(email))

    return len(users) == 1
