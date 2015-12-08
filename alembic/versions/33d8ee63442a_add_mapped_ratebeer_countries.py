"""add mapped ratebeer countries

Revision ID: 33d8ee63442a
Revises: 16a682c25f83
Create Date: 2015-12-08 19:41:49.281637

"""

# revision identifiers, used by Alembic.
revision = '33d8ee63442a'
down_revision = '16a682c25f83'
branch_labels = None
depends_on = None

import os
import json
from alembic import op
import sqlalchemy as sa


def upgrade():

    countries_table = op.create_table(
        'rb_countries_mapped',
        sa.Column('rb_id', sa.Integer, primary_key=True),
        sa.Column('rb_name', sa.Unicode(255)),
        sa.Column('iso_code', sa.Unicode(10)),
    )

    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    countries_file = os.path.join(path, 'data', 'ratebeer_countries_mapped.json')
    with open(countries_file, 'r') as countries_data:
        op.bulk_insert(countries_table, json.loads(countries_data.read()))


def downgrade():
    op.execute('DROP TABLE rb_countries_mapped')
