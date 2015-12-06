"""add unique constraint on adminareas

Revision ID: 3862fc8e9724
Revises: d5e7d6405
Create Date: 2015-12-06 16:42:27.188073

"""

# revision identifiers, used by Alembic.
revision = '3862fc8e9724'
down_revision = 'd5e7d6405'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('ALTER TABLE fylke ADD CONSTRAINT fylkesnr_unique UNIQUE (fylkesnr);')
    op.execute('ALTER TABLE kommune ADD CONSTRAINT kommnr_unique UNIQUE (kommnr);')


def downgrade():
    op.execute('ALTER TABLE fylke DROP CONSTRAINT fylkesnr_unique;')
    op.execute('ALTER TABLE kommune DROP CONSTRAINT kommnr_unique;')
