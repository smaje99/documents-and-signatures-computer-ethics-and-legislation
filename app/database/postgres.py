import sys
from asyncio import current_task
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
  AsyncSession,
  async_scoped_session,
  async_sessionmaker,
  create_async_engine,
)


__all__ = ('PostgresDatabase',)


class PostgresDatabase:
  '''Handler PostgreSQL database via SQLAlchemy.'''

  def __init__(self, db_uri: str, echo: bool) -> None:
    '''Handler PostgreSQL database via SQLAlchemy.

    Args:
      db_uri (str): URI of database.
      echo (bool): Echo flag for SQLAlchemy.

    Note:
      If database no exist, the program will exit.
    '''
    try:
      self.__engine = create_async_engine(db_uri, echo=echo)
    except SQLAlchemyError:
      sys.exit()
    else:
      self.__session_factory = async_scoped_session(
        async_sessionmaker(
          bind=self.__engine,
          autocommit=False,
          autoflush=False,
          expire_on_commit=False,
        ),
        current_task,
      )

  @asynccontextmanager
  async def session(self) -> AsyncGenerator[AsyncSession, Any]:
    '''Get a session of database.

    Raise:
      DatabaseError: Database no exist.

    Yield:
      AsyncSessionLocal: A session of database.
    '''
    session: AsyncSession = self.__session_factory()

    try:
      yield session
    except SQLAlchemyError:
      await session.rollback()
      raise
    finally:
      await session.close()
