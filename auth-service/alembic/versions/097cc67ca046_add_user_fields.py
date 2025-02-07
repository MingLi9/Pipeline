"""Add user fields 

Revision ID: 097cc67ca046
Revises: 6625c8ecd3b5
Create Date: 2024-10-27 14:56:55.248033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '097cc67ca046'
down_revision: Union[str, None] = '6625c8ecd3b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('first_name', sa.String(length=128), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(length=128), nullable=True))
    op.add_column('users', sa.Column('age', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('email', sa.String(length=255), nullable=True))
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'email')
    op.drop_column('users', 'age')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    # ### end Alembic commands ###
