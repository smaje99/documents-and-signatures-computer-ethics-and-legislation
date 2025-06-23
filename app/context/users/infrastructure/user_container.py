from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Dependency, Factory

from app.context.shared.infrastructure.persistence.sqlalchemy import OrmDao
from app.context.users.application import UserCreator
from app.context.users.domain import UserRepository
from app.context.users.infrastructure.http.api_v1 import user_endpoint
from app.context.users.infrastructure.http.api_v1.controllers import (
  UserCreatePostController,
)
from app.context.users.infrastructure.persistence.sqlalchemy import (
  OrmUserDao,
  OrmUserRepository,
)
from app.database.postgres import PostgresDatabase


class UserContainer(DeclarativeContainer):
  '''UserContainer is a dependency injection container for user-related services.

  It is used to manage the lifecycle and dependencies of user-related components.
  '''

  wiring_config = WiringConfiguration(modules=[user_endpoint])

  database = Dependency(instance_of=PostgresDatabase)

  user_dao: Factory[OrmDao] = Factory(OrmUserDao, database=database)

  user_repository: Factory[UserRepository] = Factory(OrmUserRepository, dao=user_dao)

  user_creator = Factory(UserCreator, user_repository=user_repository)

  user_create_post_controller = Factory(
    UserCreatePostController, user_creator=user_creator
  )
