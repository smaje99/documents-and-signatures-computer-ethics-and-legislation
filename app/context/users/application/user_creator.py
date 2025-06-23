from app.context.users.domain import User, UserRepository, UserSaveDto
from app.context.users.domain.user_errors import UserAlreadyExistsError


__all__ = ('UserCreator',)


class UserCreator:
  '''UserCreator is responsible for creating a new user.'''

  def __init__(self, user_repository: UserRepository):
    '''UserCreator is responsible for creating a new user.

    Args:
        user_repository (UserRepository): The user repository instance.
    '''
    self.user_repository = user_repository

  async def __call__(self, user_in: UserSaveDto) -> User:
    '''Create a new user.

    Args:
        user_in (UserSaveDto): The user data to create.

    Raises:
        UserAlreadyExistsError: If a user with the same email already exists.

    Returns:
        User: The created user.
    '''
    if await self.user_repository.contains_email(user_in.email):
      raise UserAlreadyExistsError.from_email(user_in.email)

    new_user = await self.user_repository.save(user_in)

    return new_user
