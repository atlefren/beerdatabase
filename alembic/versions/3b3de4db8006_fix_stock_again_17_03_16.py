"""fix stock again (17.03.16)

Revision ID: 3b3de4db8006
Revises: 1b434f6a7b5
Create Date: 2016-03-17 22:02:55.090285

"""

# revision identifiers, used by Alembic.
revision = '3b3de4db8006'
down_revision = '1b434f6a7b5'
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
