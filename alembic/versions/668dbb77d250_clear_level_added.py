"""clear level added

Revision ID: 668dbb77d250
Revises: 878f36410896
Create Date: 2024-08-31 13:15:07.987530

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '668dbb77d250'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('apartments', sa.Column('clear_level', sa.INTEGER(), nullable=True))


def downgrade() -> None:
    pass