"""add user table

Revision ID: 0b0198b31664
Revises: 8e136a376005
Create Date: 2023-07-03 13:55:13.239853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b0198b31664'
down_revision = '8e136a376005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('email', sa.String(), nullable=False),
                sa.Column('password', sa.String(), nullable=False),
                sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False),
                sa.PrimaryKeyConstraint('id'),
                sa.UniqueConstraint('email')
                )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
