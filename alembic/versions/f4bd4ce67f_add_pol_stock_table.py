"""add pol stock table

Revision ID: f4bd4ce67f
Revises: 4defa86894e6
Create Date: 2015-11-17 23:29:30.839431

"""

# revision identifiers, used by Alembic.
revision = 'f4bd4ce67f'
down_revision = '4defa86894e6'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'pol_shop',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(100)),
        sa.Column('street_address', sa.Unicode(100)),
        sa.Column('street_zipcode', sa.Integer),
        sa.Column('street_place', sa.Unicode(100)),
        sa.Column('post_address', sa.Unicode(100)),
        sa.Column('post_zipcode', sa.Integer),
        sa.Column('post_place', sa.Unicode(100)),
        sa.Column('phone', sa.Unicode(30)),
        sa.Column('category', sa.Integer),
        sa.Column('lon', sa.Float),
        sa.Column('lat', sa.Float),
    )

    op.create_table(
        'pol_stock',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('stock', sa.Integer),
        sa.Column('updated', sa.DateTime),
        sa.Column('shop_id', sa.Integer, sa.ForeignKey('pol_shop.id'), nullable=False),
        sa.Column('pol_beer_id', sa.Integer, sa.ForeignKey('pol_beer.id'), nullable=False)
    )


def downgrade():
    op.drop_table('pol_shop')
    op.drop_table('pol_stock')
