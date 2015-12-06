"""add geom column to pol shop table

Revision ID: 539cf8248905
Revises: 3fd9b2d19fb9
Create Date: 2015-12-06 15:48:43.979639

"""

# revision identifiers, used by Alembic.
revision = '539cf8248905'
down_revision = '3fd9b2d19fb9'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('''
    ALTER TABLE pol_shop
    ADD COLUMN geog geography(POINT,4326)
    ''')

    op.execute('UPDATE pol_shop set geog=CAST(ST_SetSRID(ST_Point(lon, lat), 4326) As geography);')


def downgrade():
    op.execute('ALTER TABLE pol_shop DROP COLUMN geog')