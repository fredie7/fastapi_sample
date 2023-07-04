"""create posts table

Revision ID: 11e2dff4a8c9
Revises: 
Create Date: 2023-07-03 13:26:43.574316

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11e2dff4a8c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
