from typing import Annotated

from pydantic import BeforeValidator

from app.context.users.domain.enums import Role


def validate_user_role(role: Role | str) -> Role:
  '''Validate user role type.

  Args:
      role (Role | str): User role.

  Returns:
      Role: Validated user role.
  '''
  assert role is not None, 'Rol del usuario es requerido'
  assert isinstance(role, (Role, str)), 'Rol del usuario no es válido'

  return Role(role) if isinstance(role, str) else role


UserRole = Annotated[Role, BeforeValidator(validate_user_role)]
'''Value object for user role type.'''
