"""add geoloc tables

Revision ID: 2b35f2f2adcb
Revises: 29474f196c96
Create Date: 2015-11-09 00:12:02.604229

"""

# revision identifiers, used by Alembic.
revision = '2b35f2f2adcb'
down_revision = '29474f196c96'
branch_labels = None
depends_on = None

import os
import json

from alembic import op
import sqlalchemy as sa


def upgrade():
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    countries_table = op.create_table(
        'rb_countries',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(255)),
    )

    countries_file = os.path.join(path, 'data', 'ratebeer_countries.json')
    with open(countries_file, 'r') as countries_data:
        op.bulk_insert(countries_table, json.loads(countries_data.read()))

    subregions_table = op.create_table(
        'rb_subregions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(255)),
    )

    subregions_file = os.path.join(path, 'data', 'ratebeer_subregions.json')
    with open(subregions_file, 'r') as subregions_data:
        op.bulk_insert(subregions_table, json.loads(subregions_data.read()))

    countrycodes_table = op.create_table(
        'country_codes',
        sa.Column('id', sa.Unicode(2), primary_key=True),
        sa.Column('name', sa.Unicode(255)),
    )

    countrycodes_file = os.path.join(path, 'data', '3166-1alpha-2.json')
    with open(countrycodes_file, 'r') as countrycodes_data:
        op.bulk_insert(countrycodes_table, json.loads(countrycodes_data.read()))


def downgrade():
    op.drop_table('rb_countries')
    op.drop_table('rb_subregions')
    op.drop_table('country_codes')
