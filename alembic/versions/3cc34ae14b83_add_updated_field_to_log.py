"""add updated-field to log

Revision ID: 3cc34ae14b83
Revises: d0fd292e452
Create Date: 2016-01-24 22:27:28.112857

"""

# revision identifiers, used by Alembic.
revision = '3cc34ae14b83'
down_revision = 'd0fd292e452'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'update_log',
        sa.Column('last_updated', sa.types.DateTime(timezone=True))
    )


def downgrade():
    op.drop_column('update_log', 'last_updated')
