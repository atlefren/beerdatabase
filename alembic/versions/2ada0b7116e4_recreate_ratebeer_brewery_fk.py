"""recreate ratebeer brewery fk

Revision ID: 2ada0b7116e4
Revises: 355bdf8fa8a7
Create Date: 2015-12-08 20:22:23.434301

"""

# revision identifiers, used by Alembic.
revision = '2ada0b7116e4'
down_revision = '355bdf8fa8a7'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    pass
    '''
    with op.batch_alter_table('rb_brewery') as batch_op:
        batch_op.drop_constraint('fk_rb_brewerys_country_rb_countries', type_='foreignkey')
    op.create_foreign_key(
        'fk_rb_brewerys_country_countries_no',
        'rb_brewery', 'countries_no',
        ['country'], ['rb_id'],
    )
    '''


def downgrade():
    pass
    '''
    with op.batch_alter_table('rb_brewery') as batch_op:
        batch_op.drop_constraint('fk_rb_brewerys_country_countries_no', type_='foreignkey')
    op.create_foreign_key(
        'fk_rb_brewerys_country_rb_countries',
        'rb_brewery', 'rb_countries',
        ['country'], ['id'],
    )
    '''
