from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Container, Singleton

from app.context.users.infrastructure.user_container import UserContainer
from app.database.postgres import PostgresDatabase


__all__ = ('ApplicationContainer',)


class ApplicationContainer(DeclarativeContainer):
  '''Application-level dependency container.'''

  config = Configuration()

  database = Singleton(
    PostgresDatabase, db_uri=config.db.uri.as_(str), echo=config.db.echo.as_(bool)
  )

  user = Container(UserContainer, database=database)
