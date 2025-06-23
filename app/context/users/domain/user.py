from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.context.users.domain.objects import UserEmail, UserId, UserRole


class User(BaseModel):
  '''User domain entity.'''

  id: UserId
  full_name: str
  email: UserEmail
  role: UserRole
  is_active: bool
  created_at: datetime

  model_config = ConfigDict(from_attributes=True, frozen=True)
