"""fix stock view

Revision ID: 152b87991b25
Revises: 4e6dee7fff64
Create Date: 2016-03-05 15:05:23.672039

"""

# revision identifiers, used by Alembic.
revision = '152b87991b25'
down_revision = '4e6dee7fff64'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('DROP VIEW pol_stock_latest')
    op.execute('CREATE VIEW pol_stock_latest AS SELECT shop_id, pol_beer_id, stock, max(updated) as updated FROM pol_stock GROUP BY shop_id, pol_beer_id, stock;')


def downgrade():
    op.execute('DROP VIEW pol_stock_latest')
