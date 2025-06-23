from fastapi import HTTPException
from starlette.status import HTTP_409_CONFLICT

from app.context.users.application import UserCreator
from app.context.users.domain import UserSaveDto
from app.context.users.domain.user_errors import UserAlreadyExistsError
from app.context.users.infrastructure.http.api_v1.controllers import (
  UserCreatePostResponse,
)


class UserCreatePostController:
  '''Post controller for handling user creation requests.'''
  def __init__(self, user_creator: UserCreator):
    '''Initializes the UserCreatePostController with a UserCreator instance.'''
    self.__user_creator = user_creator

  async def __call__(self, user_in: UserSaveDto) -> UserCreatePostResponse:
    '''Handles the user creation request.

    Args:
        user_in (UserSaveDto): The user data to be created.

    Raises:
        HTTPException: If the user already exists, raises a 409 Conflict error.

    Returns:
        UserCreatePostResponse: The response containing the created user data.
    '''
    try:
      user = await self.__user_creator(user_in)

      return UserCreatePostResponse.model_validate(user)
    except UserAlreadyExistsError as error:
      raise HTTPException(
        status_code=HTTP_409_CONFLICT, detail=error.message
      ) from error
