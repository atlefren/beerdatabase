"""use revert ibigint id for pol beer

Revision ID: 4fc1f3c2f263
Revises: 58c76602ffc2
Create Date: 2016-03-05 12:03:36.904742

"""

# revision identifiers, used by Alembic.
revision = '4fc1f3c2f263'
down_revision = '58c76602ffc2'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('pol_beer', 'id', type_=sa.types.Integer)


def downgrade():
    op.alter_column('pol_beer', 'id', type_=sa.types.BigInteger)
