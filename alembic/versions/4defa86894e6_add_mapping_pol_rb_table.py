"""add mapping pol-rb-table

Revision ID: 4defa86894e6
Revises: 461dd3f1e6e3
Create Date: 2015-11-15 18:06:12.620345

"""

# revision identifiers, used by Alembic.
revision = '4defa86894e6'
down_revision = '461dd3f1e6e3'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'pol_to_rb_mapping',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('comment', sa.Unicode(255)),
        sa.Column('resolved', sa.Boolean, default=False),
        sa.Column('rb_beer_id', sa.Integer, sa.ForeignKey('rb_beer.id'), nullable=False),
        sa.Column('pol_beer_id', sa.Integer, sa.ForeignKey('pol_beer.id'), nullable=False)
    )


def downgrade():
    op.drop_table('pol_to_rb_mapping')
