"""create OSM view

Revision ID: 1b434f6a7b5
Revises: 5a2187ce682d
Create Date: 2016-03-06 22:48:53.266525

"""

# revision identifiers, used by Alembic.
revision = '1b434f6a7b5'
down_revision = '5a2187ce682d'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('DROP VIEW IF EXISTS osm_breweries;')
    op.execute('CREATE VIEW osm_breweries AS SELECT iso.rb_id as country_id, osm.* FROM rb_brewery_position AS osm, rb_countries_mapped as iso WHERE iso.iso_code = osm.country;')


def downgrade():
    op.execute('DROP VIEW IF EXISTS osm_breweries;')
