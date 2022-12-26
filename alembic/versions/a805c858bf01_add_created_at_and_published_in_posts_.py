"""add created_at and published in posts table

Revision ID: a805c858bf01
Revises: 3999c1658d2a
Create Date: 2022-12-26 10:06:00.430900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a805c858bf01'
down_revision = '3999c1658d2a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'pubished')
    op.drop_column('posts', 'created_at')
    pass
