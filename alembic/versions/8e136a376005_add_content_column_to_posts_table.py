"""add content column to posts table

Revision ID: 8e136a376005
Revises: 11e2dff4a8c9
Create Date: 2023-07-03 13:47:25.052016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e136a376005'
down_revision = '11e2dff4a8c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
