from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column
from sqlalchemy.sql.functions import func

from app.database.mapped import (
  required_timestamp_with_timezone_and_default,
  required_uuid,
)


class IdentifierMixin(MappedAsDataclass, init=False):
  '''Common mixin for entities with a unique identifier.'''

  id: Mapped[required_uuid] = mapped_column(
    primary_key=True, default=func.uuid_generate_v4()
  )
  '''Unique identifier of the instance.'''


class CreatedTimestampMixin(MappedAsDataclass, init=False):
  '''Common mixin for entities with a creation timestamp.'''

  created_at: Mapped[required_timestamp_with_timezone_and_default]
  '''Timestamp of the instance creation.'''
