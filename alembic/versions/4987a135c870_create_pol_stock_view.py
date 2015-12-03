"""create pol stock view

Revision ID: 4987a135c870
Revises: 479a41a4f27
Create Date: 2015-12-03 21:04:35.810667

"""

# revision identifiers, used by Alembic.
revision = '4987a135c870'
down_revision = '479a41a4f27'
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.execute('CREATE VIEW pol_stock_latest AS SELECT id, shop_id, pol_beer_id, stock, max(updated) FROM pol_stock GROUP BY id, shop_id, pol_beer_id, stock;')


def downgrade():
    op.execute('DROP VIEW pol_stock_latest')
