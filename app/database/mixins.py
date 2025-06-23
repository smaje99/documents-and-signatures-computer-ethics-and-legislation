from sqlalchemy.orm import Mapped, MappedAsDataclass

from app.database.mapped import required_timestamp_with_timezone_and_default, uuid_pk


class IdentifierMixin(MappedAsDataclass, init=False):
  '''Common mixin for entities with a unique identifier.'''

  id: Mapped[uuid_pk]
  '''Unique identifier of the instance.'''


class CreatedTimestampMixin(MappedAsDataclass, init=False):
  '''Common mixin for entities with a creation timestamp.'''

  created_at: Mapped[required_timestamp_with_timezone_and_default]
  '''Timestamp of the instance creation.'''
