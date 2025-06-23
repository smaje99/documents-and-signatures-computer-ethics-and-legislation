from uuid import UUID


__all__ = ('transform_uuid',)


def transform_uuid(uuid_to_transform: str | UUID, version: int = 4) -> UUID:
  '''Transform UUID.

  Args:
      uuid_to_transform (str | UUID): UUID to transform.
      version (int): UUID version to use when parsing from string.

  Raises:
      AssertionError: If the UUID to transform is None or if the version does not match.

  Returns:
      UUID: Transformed UUID.
  '''
  assert uuid_to_transform is not None, 'UUID to transform cannot be None'

  if isinstance(uuid_to_transform, UUID):
    assert uuid_to_transform.version == version, (
      f'UUID version mismatch: expected {version}, got {uuid_to_transform.version}'
    )

    return uuid_to_transform

  return UUID(uuid_to_transform, version=version)
