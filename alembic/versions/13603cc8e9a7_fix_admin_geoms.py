"""fix admin geoms

Revision ID: 13603cc8e9a7
Revises: 307950c4e446
Create Date: 2015-12-06 22:49:57.834150

"""

# revision identifiers, used by Alembic.
revision = '13603cc8e9a7'
down_revision = '307950c4e446'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('''truncate table fylke''')
    op.execute('''truncate table kommune''')
    op.execute('''drop materialized view komm_fylke cascade''')
    op.execute('''ALTER TABLE fylke ALTER COLUMN geom TYPE geometry(MultiPolygon, 4326);''')
    op.execute('''ALTER TABLE kommune ALTER COLUMN geom TYPE geometry(MultiPolygon, 4326);''')

    op.execute('''
        CREATE MATERIALIZED VIEW komm_fylke AS
        SELECT
            k.name as name,
            k.kommnr as kommnr,
            f.name as fylke_name,
            f.fylkesnr as fylkesnr,
            k.geom as geom
        FROM
            kommune k, fylke f
        WHERE
            k.geom && f.geom;
        ''')
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
    op.execute('''truncate table fylke''')
    op.execute('''truncate table kommune''')
    op.execute('''drop materialized view komm_fylke cascade''')
    op.execute('''ALTER TABLE fylke ALTER COLUMN geom TYPE geometry(Polygon, 4326);''')
    op.execute('''ALTER TABLE kommune ALTER COLUMN geom TYPE geometry(Polygon, 4326);''')

    op.execute('''
        CREATE MATERIALIZED VIEW komm_fylke AS
        SELECT
            k.name as name,
            k.kommnr as kommnr,
            f.name as fylke_name,
            f.fylkesnr as fylkesnr,
            k.geom as geom
        FROM
            kommune k, fylke f
        WHERE
            k.geom && f.geom;
        ''')
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
