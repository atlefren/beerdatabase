"""add style foreign key

Revision ID: 29474f196c96
Revises: 1b981552bfd9
Create Date: 2015-11-08 23:50:23.806775

"""

# revision identifiers, used by Alembic.
revision = '29474f196c96'
down_revision = '1b981552bfd9'
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.create_foreign_key(
        'fk_rb_beers_style_id_style',
        'rb_beer', 'style',
        ['style_id'], ['id'],
    )


def downgrade():
    with op.batch_alter_table('rb_beer') as batch_op:
        batch_op.drop_constraint('fk_rb_beers_style_id_style', type_='foreignkey')
