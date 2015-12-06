"""create komm_fylke mview

Revision ID: 6293c753ba2
Revises: 6a38fff4b82
Create Date: 2015-12-06 17:12:25.117872

"""

# revision identifiers, used by Alembic.
revision = '6293c753ba2'
down_revision = '6a38fff4b82'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
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


def downgrade():
    op.execute('DROP MATERIALIZED VIEW komm_fylke;')
