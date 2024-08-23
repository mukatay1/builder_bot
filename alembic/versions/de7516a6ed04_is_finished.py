"""is_finished

Revision ID: de7516a6ed04
Revises: 3c6457bc4496
Create Date: 2024-08-18 21:00:23.520250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de7516a6ed04'
down_revision: Union[str, None] = '3c6457bc4496'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('apartment_stages')
    op.drop_table('apartments')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apartments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('number', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number')
    )
    op.create_table('apartment_stages',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('stage', sa.VARCHAR(length=6), nullable=False),
    sa.Column('is_ready_for_review', sa.BOOLEAN(), nullable=True),
    sa.Column('apartment_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['apartment_id'], ['apartments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
