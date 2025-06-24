from datetime import datetime
from typing import Annotated
from uuid import UUID

from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import TIMESTAMP, Text, Uuid


__all__ = (
  'text',
  'required_text',
  'required_timestamp_with_timezone_and_default',
  'required_uuid',
)


required_uuid = Annotated[UUID, mapped_column(Uuid, nullable=False)]
'''A UUID column that cannot be null, ensuring that a value is always provided.'''

text = Annotated[str, mapped_column(Text)]
'''A text column for storing string data.'''

required_text = Annotated[text, mapped_column(nullable=False)]
'''A text column that cannot be null, ensuring that a value is always provided.'''

required_timestamp_with_timezone_and_default = Annotated[
  datetime,
  mapped_column(
    TIMESTAMP(timezone=True), nullable=False, server_default=func.current_timestamp()
  ),
]
'''A timestamp column with timezone support that cannot be null and
has a default value of the current timestamp.'''
