from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED

from app.containers import ApplicationContainer
from app.context.users.domain import UserSaveDto
from app.context.users.infrastructure.http.api_v1.controllers import (
  UserCreatePostController,
  UserCreatePostResponse,
)


router = APIRouter()


@router.post('/', status_code=HTTP_201_CREATED)
@inject
async def create_user(  # noqa: D417
  user_in: Annotated[UserSaveDto, Body(alias='userIn')],
  *,
  controller: Annotated[
    UserCreatePostController,
    Depends(Provide[ApplicationContainer.user.user_create_post_controller]),
  ],
) -> UserCreatePostResponse:
  '''Create a new person with a associated user.

  If the person already exists, the user will be associated with it.

  Args:
  * userIn (UserSaveDto): User to save.

  Raises:
  * UserAlreadyExistsError: If a user with the same ID already exists.

  Returns:
  * UserCreatePostResponse: Associated user created.
  '''
  return await controller(user_in)
