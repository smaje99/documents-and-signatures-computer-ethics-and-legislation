from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator

from app.core.transformations import transform_uuid
from app.core.validations import is_valid_uuid


__all__ = ('UserId',)


def validate_user_id(user_id: UUID | str) -> UUID | str:
  '''Validate user id.

  Args:
      user_id (UUID | str): user id.

  Returns:
      UUID: Validated user id.
  '''
  assert user_id is not None, 'Id del usuario es requerido'
  assert is_valid_uuid(str(user_id)), 'Id del usuario no es válido'

  return user_id


UserId = Annotated[
  UUID, AfterValidator(validate_user_id), AfterValidator(transform_uuid)
]
