"""create rb beer table

Revision ID: 185ff7fbd78a
Revises: 3cfbd9b5d70a
Create Date: 2015-11-08 18:27:58.898174

"""

# revision identifiers, used by Alembic.
revision = '185ff7fbd78a'
down_revision = '3cfbd9b5d70a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'rb_beer',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(255)),
        sa.Column('shortname', sa.Unicode(255)),
        sa.Column('alias', sa.Boolean),
        sa.Column('retired', sa.Boolean),
        sa.Column('style_id', sa.Integer),
        sa.Column('score_overall', sa.Float),
        sa.Column('score_style', sa.Float),
        sa.Column('abv', sa.Float),
        sa.Column('ibu', sa.Float),
        sa.Column('brewery_id', sa.Integer, sa.ForeignKey('rb_brewery.id'), nullable=False),
    )


def downgrade():
    op.drop_table('rb_brewery')
