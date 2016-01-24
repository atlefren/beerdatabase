"""change update to use timestamp

Revision ID: d0fd292e452
Revises: 1617b96530fc
Create Date: 2016-01-24 17:31:53.319131

"""

# revision identifiers, used by Alembic.
revision = 'd0fd292e452'
down_revision = '1617b96530fc'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('update_log', 'datetime', type_=sa.types.DateTime(timezone=True))


def downgrade():
    op.alter_column('update_log', 'datetime', type_=sa.types.DateTime(timezone=False))
