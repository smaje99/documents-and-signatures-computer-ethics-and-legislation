from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


__all__ = ('Base',)


class Base(AsyncAttrs, MappedAsDataclass, DeclarativeBase, init=False):
  '''Base class for all SQLAlchemy models.

  The class models must have a name that starts with "Orm" and ends with "Entity".
  '''

  __name__: str

  @declared_attr.directive
  def __tablename__(cls) -> str:
    '''Generate __tablename__ automatically.'''
    return cls.__name__.removeprefix('Orm').removesuffix('Entity').lower()
