"""create pol_shop with komm and fylke view

Revision ID: 307950c4e446
Revises: 6293c753ba2
Create Date: 2015-12-06 17:17:18.624263

"""

# revision identifiers, used by Alembic.
revision = '307950c4e446'
down_revision = '6293c753ba2'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('''
    CREATE VIEW pol_shop_komm_fylke as
    SELECT
        s.*,
        k.name as komm_name,
        k.kommnr as kommnr,
        k.fylke_name as fylke_name,
        k.fylkesnr as fylkesnr
    FROM
        pol_shop s,
        komm_fylke k
    WHERE
        k.geom::geography && s.geog;
    ''')


def downgrade():
    op.execute('DROP VIEW pol_shop_komm_fylke;')
