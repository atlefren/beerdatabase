"""fix bigint fuckup

Revision ID: 569326c12e75
Revises: 4fc1f3c2f263
Create Date: 2016-03-05 14:32:43.962664

"""

# revision identifiers, used by Alembic.
revision = '569326c12e75'
down_revision = '4fc1f3c2f263'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('pol_beer', 'id', type_=sa.types.BigInteger)
    op.alter_column('pol_beer_price', 'pol_beer_id', type_=sa.types.BigInteger)


def downgrade():
    op.alter_column('pol_beer', 'id', type_=sa.types.Integer)
    op.alter_column('pol_beer_price', 'pol_beer_id', type_=sa.types.Integer)
