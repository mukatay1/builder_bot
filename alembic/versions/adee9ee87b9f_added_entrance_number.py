"""Added entrance number

Revision ID: adee9ee87b9f
Revises: bee251aed874
Create Date: 2024-09-24 04:48:35.815299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adee9ee87b9f'
down_revision: Union[str, None] = 'bee251aed874'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('apartments', sa.Column('entrance_number', sa.INTEGER(), nullable=True))



def downgrade() -> None:
    pass