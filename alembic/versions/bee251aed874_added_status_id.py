"""added status_id

Revision ID: bee251aed874
Revises: 668dbb77d250
Create Date: 2024-09-18 21:37:08.419434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bee251aed874'
down_revision: Union[str, None] = '668dbb77d250'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('apartments', sa.Column('status_id', sa.INTEGER(), nullable=True))

def downgrade() -> None:
    pass
