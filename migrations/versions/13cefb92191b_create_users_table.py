'''Create users table.

Revision ID: 13cefb92191b
Revises: 1ace91b94575
Create Date: 2025-06-22 18:00:43.054502

'''

from typing import Optional, Sequence

from alembic import op
from sqlalchemy.dialects.postgresql import ENUM, TIMESTAMP, UUID
from sqlalchemy.schema import Column, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import Boolean, Text


# revision identifiers, used by Alembic.
revision: str = '13cefb92191b'
down_revision: Optional[str] = '1ace91b94575'
branch_labels: Optional[str | Sequence[str]] = None
depends_on: Optional[str | Sequence[str]] = None


def upgrade() -> None:
  '''Upgrade method.'''
  # Create the role enum type
  op.execute('''
    CREATE TYPE user_role AS ENUM ('admin', 'user', 'verifier');
  ''')

  # Create the users table
  op.create_table(
    'users',
    Column(
      'id',
      UUID(as_uuid=True),
      nullable=False,
      server_default=func.uuid_generate_v4(),
    ),
    Column('full_name', Text, nullable=False),
    Column('email', Text, nullable=False),
    Column('hashed_password', Text, nullable=False),
    Column('public_key', Text, nullable=True),
    Column(
      'role',
      ENUM(name='user_role', create_type=False),
      nullable=False,
      server_default='user',
    ),
    Column('is_active', Boolean(), nullable=False, server_default=true()),
    Column(
      'created_at',
      TIMESTAMP(timezone=True),
      nullable=False,
      server_default=func.current_timestamp(),
    ),
    PrimaryKeyConstraint('id', name='pk_users'),
    UniqueConstraint('email', name='uq_users_email'),
    schema='public',
  )


def downgrade() -> None:
  '''Upgrade method.'''
  # Drop the users table
  op.drop_constraint('uq_users_email', 'users', schema='public')
  op.drop_constraint('pk_users', 'users', schema='public')
  op.drop_table('users', schema='public')

  # Drop the user_role enum type
  op.execute('DROP TYPE user_role;')
