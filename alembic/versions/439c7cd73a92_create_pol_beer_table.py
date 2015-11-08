"""create pol beer table

Revision ID: 439c7cd73a92
Revises: 185ff7fbd78a
Create Date: 2015-11-08 20:07:24.767824

"""

# revision identifiers, used by Alembic.
revision = '439c7cd73a92'
down_revision = '185ff7fbd78a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'pol_beer',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(255)),
        sa.Column('store_category', sa.Unicode(100)),
        sa.Column('produktutvalg', sa.Unicode(100)),
        sa.Column('producer', sa.Unicode(100)),
        sa.Column('distributor', sa.Unicode(100)),
        sa.Column('varenummer', sa.Integer),
        sa.Column('abv', sa.Float),
        sa.Column('volume', sa.Float),
        sa.Column('color', sa.Unicode(100)),
        sa.Column('smell', sa.Unicode(100)),
        sa.Column('taste', sa.Unicode(100)),
        sa.Column('method', sa.Unicode(255)),
        sa.Column('cork_type', sa.Unicode(100)),
        sa.Column('packaging_type', sa.Unicode(100)),
        sa.Column('price', sa.Float),
        sa.Column('country', sa.Unicode(100)),
        sa.Column('district', sa.Unicode(100)),
        sa.Column('subdistrict', sa.Unicode(100)),
        sa.Column('url', sa.Unicode(100)),
        sa.Column('vintage', sa.Unicode(100)),
        sa.Column('ingredients', sa.Unicode(255)),
        sa.Column('pairs_with_1', sa.Unicode(255)),
        sa.Column('pairs_with_2', sa.Unicode(255)),
        sa.Column('pairs_with_3', sa.Unicode(255)),
        sa.Column('storage_notes', sa.Unicode(255)),
        sa.Column('sweetness', sa.Integer),
        sa.Column('freshness', sa.Integer),
        sa.Column('bitterness', sa.Integer),
        sa.Column('richness', sa.Integer),
        sa.Column('ratebeer_id', sa.Integer, sa.ForeignKey('rb_beer.id'), nullable=True),
    )


def downgrade():
    op.drop_table('pol_beer')
