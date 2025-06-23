from typing import Annotated

from email_validator import EmailNotValidError, validate_email
from pydantic import AfterValidator


__all__ = ('UserEmail',)


def validate_and_transform_user_email(user_email: str) -> str:
  '''Validate and transform user's email.

  Args:
    user_email (str): user's email.

  Returns:
    str: validated and transformed user's email.
  '''
  assert (
    user_email is not None and len(user_email.strip()) > 0
  ), 'Correo electrónico del usuario es requerido.'

  try:
    email_info = validate_email(user_email.strip(), check_deliverability=False)
    return email_info.email
  except EmailNotValidError as error:
    assert not error, 'Correo electrónico del usuario no es válido.'

    return user_email


UserEmail = Annotated[str, AfterValidator(validate_and_transform_user_email)]
'''Value object user's email.'''
