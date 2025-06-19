'''${message}.

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

'''
from typing import Sequence, Optional

import sqlalchemy as sa
from alembic import op
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Optional[str] = ${repr(down_revision)}
branch_labels: Optional[str | Sequence[str]] = ${repr(branch_labels)}
depends_on: Optional[str | Sequence[str]] = ${repr(depends_on)}


def upgrade() -> None:
    '''Upgrade method.'''
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    '''Upgrade method.'''
    ${downgrades if downgrades else "pass"}
