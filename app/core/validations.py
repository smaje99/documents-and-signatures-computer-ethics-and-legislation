from uuid import UUID


__all__ = ('is_valid_uuid',)


def is_valid_uuid(uuid_to_test: str, version: int = 4) -> bool:
  '''Validate uuid.

  Args:
      uuid_to_test (str): UUID to test.
      version (int, optional): Version. Defaults to 4.

  Returns:
      bool: Is valid.
  '''
  try:
    uuid_obj = UUID(uuid_to_test, version=version)
  except ValueError:
    return False

  return str(uuid_obj) == uuid_to_test.lower() and uuid_obj.version == version
