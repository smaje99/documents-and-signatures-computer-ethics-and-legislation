import re
from typing import Annotated, Final

from pydantic import BeforeValidator


__all__ = ('UserPassword',)


MIN_PASSWORD_LENGTH: Final[int] = 8
SPECIAL_CHARACTERS: Final[str] = '!@#$%^&*()-_=+[]{}|;:,.<>?/'


def validate_and_transform_user_password(user_password: str) -> str:
  '''Validate and transform user's password.

  Args:
      user_password (str): user's password.

  Returns:
      str: validated and transformed user's password.
  '''
  assert user_password is not None and len(user_password.strip()) > 0, (
    'La contraseña del usuario es requerida.'
  )
  assert user_password.strip() != 'password', 'La contraseña no puede ser "password".'
  assert len(user_password.strip()) >= MIN_PASSWORD_LENGTH, (
    f'La contraseña debe tener al menos {MIN_PASSWORD_LENGTH} caracteres.'
  )
  assert re.search(r'\d', user_password), (
    'La contraseña debe contener al menos un dígito.'
  )
  assert re.search(r'[A-Z]', user_password), (
    'La contraseña debe contener al menos una letra mayúscula.'
  )
  assert re.search(r'[a-z]', user_password), (
    'La contraseña debe contener al menos una letra minúscula.'
  )
  assert re.search(f'[{re.escape(SPECIAL_CHARACTERS)}]', user_password), (
    'La contraseña debe contener al menos un carácter especial.'
  )

  return user_password.strip()


UserPassword = Annotated[str, BeforeValidator(validate_and_transform_user_password)]
'''Value object user's password.'''
