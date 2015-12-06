"""create admin area tables

Revision ID: d5e7d6405
Revises: 539cf8248905
Create Date: 2015-12-06 16:21:47.688673

"""

# revision identifiers, used by Alembic.
revision = 'd5e7d6405'
down_revision = '539cf8248905'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('''
    CREATE TABLE fylke (
        id serial PRIMARY KEY,
        fylkesnr int,
        name varchar(255),
        geom geometry(Polygon, 4326)
    )
    ''')
    op.execute('''
    CREATE TABLE kommune (
        id serial PRIMARY KEY,
        kommnr int,
        name varchar(255),
        geom geometry(Polygon, 4326)
    )
    ''')



def downgrade():
    op.execute('DROP TABLE fylke')
    op.execute('DROP TABLE kommune')
