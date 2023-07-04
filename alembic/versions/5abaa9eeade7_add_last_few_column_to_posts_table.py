"""add last few column to posts table

Revision ID: 5abaa9eeade7
Revises: 75e81b2ba9fb
Create Date: 2023-07-04 11:23:04.113615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5abaa9eeade7'
down_revision = '75e81b2ba9fb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
