"""add added date to pol beer

Revision ID: 100a26a2dfc5
Revises: 3cc34ae14b83
Create Date: 2016-02-02 23:36:44.157993

"""

# revision identifiers, used by Alembic.
revision = '100a26a2dfc5'
down_revision = '3cc34ae14b83'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'pol_beer',
        sa.Column('created', sa.types.DateTime(timezone=True))
    )


def downgrade():
    op.drop_column('pol_beer', 'created')
