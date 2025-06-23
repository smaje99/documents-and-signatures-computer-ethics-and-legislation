__all__ = ('enum_values_callable',)

def enum_values_callable(obj):
  '''Extracts the values of an enum object.'''
  return [e.value for e in obj]
