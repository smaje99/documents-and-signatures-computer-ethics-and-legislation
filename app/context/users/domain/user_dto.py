from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.context.users.domain.enums import Role
from app.context.users.domain.objects import UserRole


__all__ = ('UserSaveDto',)


class UserSaveDto(BaseModel):
  '''Data Transfer Object for saving user information.'''
  full_name: str
  email: str
  password: str
  role: UserRole = Role.USER

  model_config = ConfigDict(alias_generator=to_camel, frozen=True)
