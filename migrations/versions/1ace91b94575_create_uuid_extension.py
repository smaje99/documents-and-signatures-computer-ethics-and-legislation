'''Create uuid extension.

Revision ID: 1ace91b94575
Revises:
Create Date: 2025-06-22 17:43:59.631230

'''
from typing import Optional, Sequence

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '1ace91b94575'
down_revision: Optional[str] = None
branch_labels: Optional[str | Sequence[str]] = None
depends_on: Optional[str | Sequence[str]] = None


def upgrade() -> None:
    '''Upgrade method.'''
    # Create the uuid extension if it does not already exist.
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')


def downgrade() -> None:
    '''Upgrade method.'''
    # Drop the uuid extension if it exists.
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
