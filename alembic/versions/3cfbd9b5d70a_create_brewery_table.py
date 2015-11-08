"""create brewery table

Revision ID: 3cfbd9b5d70a
Revises: 
Create Date: 2015-11-08 17:42:06.858901

"""

# revision identifiers, used by Alembic.
revision = '3cfbd9b5d70a'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'rb_brewery',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(255)),
        sa.Column('country', sa.Integer),
        sa.Column('subregion', sa.Integer),
        sa.Column('city', sa.Unicode(255)),
    )


def downgrade():
    op.drop_table('rb_brewery')
