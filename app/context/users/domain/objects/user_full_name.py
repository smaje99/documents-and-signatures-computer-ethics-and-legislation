from typing import Annotated

from pydantic import AfterValidator


__all__ = ('UserFullName',)


def validate_and_transform_user_full_name(user_full_name: str) -> str:
    '''Validate and transform user's full name.

    Args:
        user_full_name (str): user's full name.

    Returns:
        str: validated and transformed user's full name.
    '''
    assert (
        user_full_name is not None and len(user_full_name.strip()) > 0
    ), 'Nombre completo del usuario es requerido.'

    return user_full_name.strip().title()


UserFullName = Annotated[str, AfterValidator(validate_and_transform_user_full_name)]
'''Value object user's full name.'''
