from asyncio import current_task
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
  AsyncEngine,
  AsyncSession,
  async_scoped_session,
  async_sessionmaker,
  create_async_engine,
)
from sqlalchemy.orm import declarative_base


__all__ = ('session',)


Base = declarative_base()

DATABASE_URL = 'sqlite+aiosqlite:///./database.db'

__engine: AsyncEngine = create_async_engine(
  DATABASE_URL,
  echo=True,  # Change to False in production
  future=True,
)

__session_factory = async_scoped_session(
  async_sessionmaker(
    bind=__engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
  ),
  current_task,
)

@asynccontextmanager
async def session() -> AsyncGenerator[AsyncSession, Any]:
  '''Get a async session of database.

  Yields:
      Iterator[AsyncGenerator[AsyncSession, Any]]: A session of database.
  '''
  session: AsyncSession = __session_factory()

  try:
    yield session
  except SQLAlchemyError:
    await session.rollback()
    raise
  finally:
    await session.close()
