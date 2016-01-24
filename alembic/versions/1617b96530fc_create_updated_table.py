"""create updated table

Revision ID: 1617b96530fc
Revises: 5123489dfc7c
Create Date: 2016-01-24 17:24:16.020354

"""

# revision identifiers, used by Alembic.
revision = '1617b96530fc'
down_revision = '5123489dfc7c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'update_log',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('type', sa.Unicode(255)),
        sa.Column('datetime', sa.DateTime)
    )


def downgrade():
    op.drop_table('update_log')
