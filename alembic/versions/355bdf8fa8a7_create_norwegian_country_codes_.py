"""create norwegian country codes materialized view

Revision ID: 355bdf8fa8a7
Revises: abe8137602a
Create Date: 2015-12-08 20:07:58.804272

"""

# revision identifiers, used by Alembic.
revision = '355bdf8fa8a7'
down_revision = 'abe8137602a'
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.execute('''
    CREATE MATERIALIZED VIEW countries_no AS (
        SELECT
            r.rb_id, i.name, i.iso_code
        FROM
            country_codes_no i, rb_countries_mapped r
        WHERE
            r.iso_code = r.iso_code);
    ''')


def downgrade():
    op.execute('DROP MATERIALIZED VIEW countries_no;')
