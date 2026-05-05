"""add_deleted_at_to_areas

Revision ID: f5b3589a115e
Revises: add_performance_indexes
Create Date: 2026-04-20 14:49:38.025791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5b3589a115e'
down_revision: Union[str, None] = 'add_performance_indexes'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('areas', sa.Column('deleted_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('areas', 'deleted_at')
