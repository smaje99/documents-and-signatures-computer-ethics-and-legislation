from abc import ABCMeta, abstractmethod

from app.context.users.domain import User, UserId, UserSaveDto


__all__ = ('UserRepository',)


class UserRepository(metaclass=ABCMeta):
  '''User repository.'''

  @abstractmethod
  async def save(self, user_in: UserSaveDto) -> User:
    '''Save a new user.

    Args:
        user_in (UserSaveDto): New user data.

    Returns:
        User: Saved user.
    '''

  @abstractmethod
  async def contains(self, user_id: UserId) -> bool:
    '''Check if a user exists.

    Args:
        user_id (UserId): User id.

    Returns:
        bool: True if user exists, False otherwise.
    '''

  @abstractmethod
  async def contains_email(self, email: str) -> bool:
    '''Check if a user with the given email exists.

    Args:
        email (str): User email.

    Returns:
        bool: True if user with the given email exists, False otherwise.
    '''
