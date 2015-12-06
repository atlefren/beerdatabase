"""add spatial indices

Revision ID: 6a38fff4b82
Revises: 3862fc8e9724
Create Date: 2015-12-06 16:56:25.578982

"""

# revision identifiers, used by Alembic.
revision = '6a38fff4b82'
down_revision = '3862fc8e9724'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('CREATE INDEX fylke_geom_gix ON fylke USING GIST (geom);')
    op.execute('CREATE INDEX kommune_geom_gix ON kommune USING GIST (geom);')
    op.execute('CREATE INDEX pol_shop_geog_gix ON pol_shop USING GIST (geog);')


def downgrade():
    op.execute('DROP INDEX fylke_geom_gix;')
    op.execute('DROP INDEX kommune_geom_gix;')
    op.execute('DROP INDEX pol_shop_geog_gix;')
