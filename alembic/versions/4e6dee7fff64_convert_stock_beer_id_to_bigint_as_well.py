"""convert stock beer id to bigint as well

Revision ID: 4e6dee7fff64
Revises: 569326c12e75
Create Date: 2016-03-05 14:47:44.245190

"""

# revision identifiers, used by Alembic.
revision = '4e6dee7fff64'
down_revision = '569326c12e75'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('DROP VIEW pol_stock_latest')
    op.alter_column('pol_stock', 'pol_beer_id', type_=sa.types.BigInteger)
    op.execute('CREATE VIEW pol_stock_latest AS SELECT id, shop_id, pol_beer_id, stock, max(updated) FROM pol_stock GROUP BY id, shop_id, pol_beer_id, stock;')


def downgrade():
    op.execute('DROP VIEW pol_stock_latest')
    op.alter_column('pol_stock', 'pol_beer_id', type_=sa.types.Integer)
    op.execute('CREATE VIEW pol_stock_latest AS SELECT id, shop_id, pol_beer_id, stock, max(updated) FROM pol_stock GROUP BY id, shop_id, pol_beer_id, stock;')
