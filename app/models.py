from datetime import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, LargeBinary, String, Text

from app.database import Base


uuid_pk = Annotated[
  str,
  mapped_column(
    Text, primary_key=True, nullable=False, comment='UUID4 primary key, stored as string'
  ),
]

required_timestamp_default = Annotated[
  datetime,
  mapped_column(
    BigInteger,
    nullable=False,
    server_default=text("(strftime('%s', 'now'))"),  # Unix timestamp in seconds
    comment='Timestamp in Unix time (seconds)',
  ),
]


class Consent(Base):
  '''Model for storing user consents in the database.'''

  __tablename__ = 'consents'

  id: Mapped[uuid_pk]
  user: Mapped[str] = mapped_column(String(100), nullable=False)
  timestamp: Mapped[required_timestamp_default]


class Contract(Base):
  '''Model for storing user contracts in the database.'''

  __tablename__ = 'contracts'

  id: Mapped[uuid_pk]
  content: Mapped[str] = mapped_column(Text, nullable=False)
  created_at: Mapped[required_timestamp_default]

  signatures: Mapped[list['Signature']] = relationship(back_populates='contract')


class Signature(Base):
  '''Model for storing user signatures in the database.'''

  __tablename__ = 'signatures'

  id: Mapped[uuid_pk]
  contract_id: Mapped[str] = mapped_column(ForeignKey('contracts.id'), nullable=False)
  signature: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
  verified: Mapped[bool] = mapped_column(
    Boolean,
    server_default=text('0'),
    nullable=False,
  )
  verified_at: Mapped[required_timestamp_default]

  contract: Mapped['Contract'] = relationship(back_populates='signatures')


class AuditLog(Base):
  '''Model for storing audit logs in the database.'''

  __tablename__ = 'audit_logs'

  id: Mapped[uuid_pk]
  action: Mapped[str] = mapped_column(String(255), nullable=False)
  details: Mapped[str] = mapped_column(Text)
  timestamp: Mapped[required_timestamp_default]
