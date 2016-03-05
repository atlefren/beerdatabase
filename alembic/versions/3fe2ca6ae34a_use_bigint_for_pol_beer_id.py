"""use bigint for pol beer id

Revision ID: 3fe2ca6ae34a
Revises: 51712c35b178
Create Date: 2016-03-05 11:48:20.627273

"""

# revision identifiers, used by Alembic.
revision = '3fe2ca6ae34a'
down_revision = '51712c35b178'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('pol_beer', 'id', type_=sa.types.BigInteger)


def downgrade():
    op.alter_column('pol_beer', 'id', type_=sa.types.Integer)
