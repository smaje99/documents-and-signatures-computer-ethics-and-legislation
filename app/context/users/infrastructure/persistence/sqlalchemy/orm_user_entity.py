from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.sqltypes import Boolean

from app.context.users.domain.enums import Role
from app.database.base import Base
from app.database.mapped import required_text, text
from app.database.mixins import CreatedTimestampMixin, IdentifierMixin
from app.database.utils import enum_values_callable


__all__ = ('OrmUserEntity',)


class OrmUserEntity(Base, IdentifierMixin, CreatedTimestampMixin):
  '''ORM entity for User.

  This class represents the User entity in the SQLAlchemy ORM.
  It inherits from Base and IdentifierMixin to provide a unique identifier.
  It also inherits from CreatedTimestampMixin to automatically manage the
  creation timestamp.
  '''

  full_name: Mapped[required_text]

  email: Mapped[required_text]

  password_hash: Mapped[required_text]

  public_key: Mapped[text]

  role: Mapped[Role] = mapped_column(
    ENUM(Role, create_type=False, values=enum_values_callable),
    nullable=False,
    server_default='user'
  )

  is_active: Mapped[bool] = mapped_column(
    Boolean, nullable=False, server_default=true()
  )
