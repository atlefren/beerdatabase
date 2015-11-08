"""add position fks

Revision ID: 461dd3f1e6e3
Revises: 2b35f2f2adcb
Create Date: 2015-11-09 00:24:19.278315

"""

# revision identifiers, used by Alembic.
revision = '461dd3f1e6e3'
down_revision = '2b35f2f2adcb'
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.create_foreign_key(
        'fk_rb_brewerys_country_rb_countries',
        'rb_brewery', 'rb_countries',
        ['country'], ['id'],
    )

    op.create_foreign_key(
        'fk_rb_brewerys_subregion_rb_subregions',
        'rb_brewery', 'rb_subregions',
        ['subregion'], ['id'],
    )


def downgrade():
    with op.batch_alter_table('rb_brewery') as batch_op:
        batch_op.drop_constraint('fk_rb_brewerys_country_rb_country', type_='foreignkey')
    with op.batch_alter_table('rb_brewery') as batch_op:
        batch_op.drop_constraint('fk_rb_brewerys_subregion_rb_subregions', type_='foreignkey')
