"""redefine pol stock view

Revision ID: 1ce7dfb467e9
Revises: 4987a135c870
Create Date: 2015-12-03 21:18:39.483164

"""

# revision identifiers, used by Alembic.
revision = '1ce7dfb467e9'
down_revision = '4987a135c870'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('DROP VIEW pol_stock_latest')
    op.execute('CREATE VIEW pol_stock_latest AS SELECT id, shop_id, pol_beer_id, stock, max(updated) as updated FROM pol_stock GROUP BY id, shop_id, pol_beer_id, stock;')


def downgrade():
    op.execute('DROP VIEW pol_stock_latest')
