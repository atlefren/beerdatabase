"""expand osm brewery table

Revision ID: 5a2187ce682d
Revises: 152b87991b25
Create Date: 2016-03-06 22:11:09.092938

"""

# revision identifiers, used by Alembic.
revision = '5a2187ce682d'
down_revision = '152b87991b25'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('rb_brewery_position', sa.Column('website', sa.String()),)
    op.add_column('rb_brewery_position', sa.Column('amenity', sa.String()),)
    op.add_column('rb_brewery_position', sa.Column('housenumber', sa.String()),)
    op.add_column('rb_brewery_position', sa.Column('city', sa.String()),)
    op.add_column('rb_brewery_position', sa.Column('postcode', sa.String()),)
    op.add_column('rb_brewery_position', sa.Column('street', sa.String()),)
    op.add_column('rb_brewery_position', sa.Column('country', sa.String()),)
    op.add_column('rb_brewery_position', sa.Column('name', sa.String()),)
    op.add_column('rb_brewery_position', sa.Column('operator', sa.String()),)


def downgrade():
    op.drop_column('rb_brewery_position', 'website')
    op.drop_column('rb_brewery_position', 'amenity')
    op.drop_column('rb_brewery_position', 'housenumber')
    op.drop_column('rb_brewery_position', 'city')
    op.drop_column('rb_brewery_position', 'postcode')
    op.drop_column('rb_brewery_position', 'street')
    op.drop_column('rb_brewery_position', 'country')
    op.drop_column('rb_brewery_position', 'name')
    op.drop_column('rb_brewery_position', 'operator')
