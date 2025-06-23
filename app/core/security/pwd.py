from typing import Final

from passlib.context import CryptContext


__all__ = ('get_password_hash', 'verify_password')


pwd_context: Final[CryptContext] = CryptContext(
  schemes=['bcrypt', 'des_crypt'], default='bcrypt', deprecated='auto'
)


def get_password_hash(password: str) -> str:
  '''Generates a hash from password encryption.

  Args:
      password (str): Password to encrypt.

  Returns:
      str: Hashed password.
  '''
  return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
  '''Verify if a plain password matches an hashed password.

  Args:
      plain_password (str): Plain password.
      hashed_password (str): Hashed password.

  Returns:
      bool: True if the password match, otherwise False.
  '''
  return pwd_context.verify(plain_password, hashed_password)
