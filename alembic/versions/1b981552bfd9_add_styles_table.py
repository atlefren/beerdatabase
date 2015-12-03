"""add styles table

Revision ID: 1b981552bfd9
Revises: 439c7cd73a92
Create Date: 2015-11-08 23:43:05.572097

"""


# revision identifiers, used by Alembic.
revision = '1b981552bfd9'
down_revision = '439c7cd73a92'
branch_labels = None
depends_on = None

import os
import json

from alembic import op
import sqlalchemy as sa


def upgrade():
    style_table = op.create_table(
        'style',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(255)),
    )
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    style_file = os.path.join(path, 'data', 'beer_styles.json')
    with open(style_file, 'r') as styles_data:
        styles = json.loads(styles_data.read())
        op.bulk_insert(style_table, styles)


def downgrade():
    op.drop_table('style')
