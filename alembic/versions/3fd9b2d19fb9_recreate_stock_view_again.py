"""recreate stock view again

Revision ID: 3fd9b2d19fb9
Revises: 1ce7dfb467e9
Create Date: 2015-12-04 00:15:27.088541

"""

# revision identifiers, used by Alembic.
revision = '3fd9b2d19fb9'
down_revision = '1ce7dfb467e9'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('DROP VIEW pol_stock_latest')
    op.execute('CREATE VIEW pol_stock_latest AS SELECT shop_id, pol_beer_id, stock, max(updated) as updated FROM pol_stock GROUP BY shop_id, pol_beer_id, stock;')


def downgrade():
    op.execute('DROP VIEW pol_stock_latest')
