from enum import StrEnum


__all__ = ('Role',)


class Role(StrEnum):
  '''Enumeration for roles in the system.'''

  ADMIN = 'admin'
  USER = 'user'
  VERIFIER = 'verifier'
