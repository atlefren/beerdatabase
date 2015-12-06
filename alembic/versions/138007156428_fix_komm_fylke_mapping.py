"""fix komm fylke mapping

Revision ID: 138007156428
Revises: 13603cc8e9a7
Create Date: 2015-12-06 23:12:25.241712

"""

# revision identifiers, used by Alembic.
revision = '138007156428'
down_revision = '13603cc8e9a7'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('DROP MATERIALIZED VIEW komm_fylke CASCADE;')
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
            k.geom && f.geom
        AND
            st_contains(f.geom, k.geom)
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
        k.geom::geography && s.geog
    AND
        st_contains(k.geom, s.geog::geometry);
    ''')


def downgrade():
    pass
