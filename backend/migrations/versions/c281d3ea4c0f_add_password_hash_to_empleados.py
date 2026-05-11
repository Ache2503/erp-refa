"""Add password_hash to empleados

Revision ID: c281d3ea4c0f
Revises: b30940f0877b
Create Date: 2026-05-09 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c281d3ea4c0f'
down_revision: Union[str, None] = 'b30940f0877b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('empleados', sa.Column('password_hash', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('empleados', 'password_hash')
