"""use bigint for osm id in  brewery position

Revision ID: 357280d45e18
Revises: 113656134776
Create Date: 2016-02-03 01:41:21.681676

"""

# revision identifiers, used by Alembic.
revision = '357280d45e18'
down_revision = '113656134776'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('''ALTER TABLE rb_brewery_position ALTER COLUMN osm_id TYPE bigint;''')


def downgrade():
    op.execute('''ALTER TABLE rb_brewery_position ALTER COLUMN osm_id TYPE int;''')
