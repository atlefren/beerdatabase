"""add price history table for pol beer

Revision ID: 59535009c19f
Revises: 100a26a2dfc5
Create Date: 2016-02-02 23:52:05.191935

"""

# revision identifiers, used by Alembic.
revision = '59535009c19f'
down_revision = '100a26a2dfc5'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'pol_beer_price',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('pol_beer_id', sa.Integer, sa.ForeignKey('pol_beer.id'), nullable=False),
        sa.Column('price', sa.Float),
        sa.Column('updated', sa.DateTime(timezone=True))
    )


def downgrade():
    op.drop_table('pol_beer_price')
