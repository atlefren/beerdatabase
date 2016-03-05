"""use bigint for pol beer varenummer

Revision ID: 58c76602ffc2
Revises: 3fe2ca6ae34a
Create Date: 2016-03-05 11:54:37.248258

"""

# revision identifiers, used by Alembic.
revision = '58c76602ffc2'
down_revision = '3fe2ca6ae34a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('pol_beer', 'varenummer', type_=sa.types.BigInteger)


def downgrade():
    op.alter_column('pol_beer', 'varenummer', type_=sa.types.Integer)
