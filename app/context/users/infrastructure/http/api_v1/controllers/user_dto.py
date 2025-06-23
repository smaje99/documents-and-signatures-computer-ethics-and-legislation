from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.context.users.domain.enums import Role


__all__ = ('UserCreatePostResponse',)


class UserCreatePostResponse(BaseModel):
  '''Response DTO for user creation.'''

  id: int
  fullname: str
  email: str
  role: Role
  is_active: bool
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)
