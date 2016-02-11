"""create country_geom table

Revision ID: 51712c35b178
Revises: 357280d45e18
Create Date: 2016-02-09 22:36:54.257145

"""
import os
import json

# revision identifiers, used by Alembic.
revision = '51712c35b178'
down_revision = '357280d45e18'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():

    countrygeom_table = op.create_table(
        'country_geom',
        sa.Column('iso_code', sa.Unicode(4), primary_key=True),
        sa.Column('continent', sa.Unicode(255)),
        sa.Column('geom_text', sa.Text()),
    )
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    country_file = os.path.join(path, 'data', 'ne_50m_admin_0_countries.geojson')
    print '!!'
    with open(country_file, 'r') as country_data:
        data = [{
            'iso_code': feature['properties']['iso_a2'],
            'continent': feature['properties']['continent'],
            'geom_text': json.dumps(feature['geometry']),
        } for feature in json.loads(country_data.read())['features'] if feature['properties']['iso_a2'] != '-99']
        print len(data)
        op.bulk_insert(countrygeom_table, data)
    op.execute('''
        ALTER TABLE country_geom
        ADD COLUMN geog geography(GEOMETRY,4326)
    ''')
    op.execute('''
        UPDATE country_geom
        SET geog=ST_GeomFromGeoJSON(geom_text)::geography
    ''')
    op.execute('''
        ALTER TABLE country_geom
        DROP COLUMN geom_text
    ''')

def downgrade():
    op.execute('DROP TABLE country_geom;')
