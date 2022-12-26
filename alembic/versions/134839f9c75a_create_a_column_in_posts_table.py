"""create a column in posts table

Revision ID: 134839f9c75a
Revises: 3aaab432e6c2
Create Date: 2022-12-22 10:42:04.292488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '134839f9c75a'
down_revision = '3aaab432e6c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
