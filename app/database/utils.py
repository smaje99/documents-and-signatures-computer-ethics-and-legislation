from enum import Enum


__all__ = ('enum_values_callable',)


def enum_values_callable(obj: type[Enum]) -> list[str]:
  '''Extracts the values of an enum object.'''
  return [e.value for e in obj.__members__.values()]
