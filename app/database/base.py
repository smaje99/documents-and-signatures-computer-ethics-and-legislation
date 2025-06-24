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
    '''Generate __tablename__ automatically in plural form.'''
    name = cls.__name__.removeprefix('Orm').removesuffix('Entity').lower()

    # Simple pluralization: add 'es' if ends with 's', 'x', 'z', 'ch', 'sh', else add 's'
    if name.endswith(('s', 'x', 'z', 'ch', 'sh')):
        return name + 'es'
    elif name.endswith('y') and name[-2] not in 'aeiou':
        return name[:-1] + 'ies'
    else:
        return name + 's'
