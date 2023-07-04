"""add foreign-key to post table

Revision ID: 75e81b2ba9fb
Revises: 0b0198b31664
Create Date: 2023-07-04 11:10:09.582542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75e81b2ba9fb'
down_revision = '0b0198b31664'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts','owner_id')
    pass
