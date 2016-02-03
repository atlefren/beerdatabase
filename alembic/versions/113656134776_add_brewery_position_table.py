"""add brewery position table

Revision ID: 113656134776
Revises: 59535009c19f
Create Date: 2016-02-03 01:01:04.606575

"""

# revision identifiers, used by Alembic.
revision = '113656134776'
down_revision = '59535009c19f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.execute('''
    CREATE TABLE rb_brewery_position (
        osm_id int PRIMARY KEY,
        ratebeer_id int,
        geom geometry(Point, 4326),
        CONSTRAINT rb_brewery_position_ratebeer_id_fkey FOREIGN KEY (ratebeer_id)
        REFERENCES public.rb_brewery (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
    );
    ''')

def downgrade():
    op.execute('DROP TABLE rb_brewery_position;')
