"""recreate no country codes mview

Revision ID: 5123489dfc7c
Revises: 17a6e4a91778
Create Date: 2015-12-08 20:44:01.602569

"""

# revision identifiers, used by Alembic.
revision = '5123489dfc7c'
down_revision = '17a6e4a91778'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('DROP MATERIALIZED VIEW countries_no')
    op.execute('''
    CREATE MATERIALIZED VIEW countries_no AS (
        SELECT
            r.rb_id, i.name, i.iso_code
        FROM
            country_codes_no i, rb_countries_mapped r
        WHERE
            r.iso_code = i.iso_code);
    ''')


def downgrade():
    pass
