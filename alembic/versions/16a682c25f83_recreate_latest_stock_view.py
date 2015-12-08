"""recreate latest stock view

Revision ID: 16a682c25f83
Revises: 138007156428
Create Date: 2015-12-08 01:10:22.535435

"""

# revision identifiers, used by Alembic.
revision = '16a682c25f83'
down_revision = '138007156428'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('DROP VIEW pol_stock_latest;')
    op.execute('''
        CREATE VIEW pol_stock_latest as
            SELECT DISTINCT ON (pol_beer_id, shop_id) shop_id, pol_beer_id, stock, updated
            FROM pol_stock
            ORDER BY pol_beer_id, shop_id, updated DESC;
    ''')


def downgrade():
    pass
