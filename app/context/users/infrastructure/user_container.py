from dependency_injector.containers import DeclarativeContainer  # type: ignore
from dependency_injector.providers import Dependency, Factory

from app.context.shared.infrastructure.persistence.sqlalchemy import OrmDao
from app.context.users.application import UserCreator
from app.context.users.domain.user_repository import UserRepository
from app.context.users.infrastructure.persistence.sqlalchemy import (
  OrmUserDao,
  OrmUserRepository,
)
from app.database.postgres import PostgresDatabase


class UserContainer(DeclarativeContainer):
  '''UserContainer is a dependency injection container for user-related services.

  It is used to manage the lifecycle and dependencies of user-related components.
  '''

  database = Dependency(instance_of=PostgresDatabase)

  user_dao: Factory[OrmDao] = Factory(OrmUserDao, database=database)

  user_repository: Factory[UserRepository] = Factory(OrmUserRepository, dao=user_dao)

  user_creator = Factory(UserCreator, user_repository=user_repository)
