"""Autoincrement id

Revision ID: 16ded13136a6
Revises: 7c9b52d3ec01
Create Date: 2024-10-27 19:47:53.851672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16ded13136a6'
down_revision: Union[str, None] = '7c9b52d3ec01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
