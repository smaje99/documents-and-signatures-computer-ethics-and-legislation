from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.context.users.domain.objects import (
  UserEmail,
  UserFullName,
  UserId,
  UserPassword,
  UserRole,
)


class User(BaseModel):
  '''User domain entity.'''

  id: UserId
  full_name: UserFullName
  email: UserEmail
  password_hash: UserPassword
  role: UserRole
  is_active: bool
  created_at: datetime

  model_config = ConfigDict(from_attributes=True, frozen=True)
