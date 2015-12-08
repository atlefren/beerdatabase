"""add norwegian iso country codes

Revision ID: abe8137602a
Revises: 33d8ee63442a
Create Date: 2015-12-08 20:02:30.906946

"""

# revision identifiers, used by Alembic.
revision = 'abe8137602a'
down_revision = '33d8ee63442a'
branch_labels = None
depends_on = None

import os
import json
from alembic import op
import sqlalchemy as sa


def upgrade():
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    countrycodes_table = op.create_table(
        'country_codes_no',
        sa.Column('iso_code', sa.Unicode(2), primary_key=True),
        sa.Column('name', sa.Unicode(255)),
    )
    countrycodes_file = os.path.join(path, 'data', '3166-1alpha-2_no.json')
    with open(countrycodes_file, 'r') as countrycodes_data:
        op.bulk_insert(countrycodes_table, json.loads(countrycodes_data.read()))


def downgrade():
    op.drop_table('country_codes_no')
