"""extend pol shop table

Revision ID: 479a41a4f27
Revises: f4bd4ce67f
Create Date: 2015-11-18 23:56:57.919120

"""

# revision identifiers, used by Alembic.
revision = '479a41a4f27'
down_revision = 'f4bd4ce67f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('ALTER TABLE pol_shop ALTER COLUMN post_zipcode TYPE varchar(10);')

    op.add_column(
        'pol_shop',
        sa.Column('weeknum', sa.String()),
    )
    op.add_column(
        'pol_shop',
        sa.Column('open_monday', sa.String()),
    )
    op.add_column(
        'pol_shop',
        sa.Column('open_tuesday', sa.String()),
    )
    op.add_column(
        'pol_shop',
        sa.Column('open_wednesday', sa.String()),
    )
    op.add_column(
        'pol_shop',
        sa.Column('open_thursday', sa.String()),
    )
    op.add_column(
        'pol_shop',
        sa.Column('open_friday', sa.String()),
    )
    op.add_column(
        'pol_shop',
        sa.Column('open_saturday', sa.String()),
    )

    op.add_column(
        'pol_shop',
        sa.Column('weeknum_next', sa.String()),
    )
    op.add_column(
        'pol_shop',
        sa.Column('open_monday_next', sa.String()),
    )
    op.add_column(
        'pol_shop',
        sa.Column('open_tuesday_next', sa.String()),
    )
    op.add_column(
        'pol_shop',
        sa.Column('open_wednesday_next', sa.String()),
    )
    op.add_column(
        'pol_shop',
        sa.Column('open_thursday_next', sa.String()),
    )
    op.add_column(
        'pol_shop',
        sa.Column('open_friday_next', sa.String()),
    )
    op.add_column(
        'pol_shop',
        sa.Column('open_saturday_next', sa.String()),
    )


def downgrade():
    op.execute('ALTER TABLE pol_shop ALTER COLUMN post_zipcode TYPE integer USING (post_zipcode::integer);')

    op.drop_column('pol_shop', 'weeknum')
    op.drop_column('pol_shop', 'open_monday')
    op.drop_column('pol_shop', 'open_tuesday')
    op.drop_column('pol_shop', 'open_wednesday')
    op.drop_column('pol_shop', 'open_thursday')
    op.drop_column('pol_shop', 'open_friday')
    op.drop_column('pol_shop', 'open_saturday')
    op.drop_column('pol_shop', 'weeknum_next')
    op.drop_column('pol_shop', 'open_monday_next')
    op.drop_column('pol_shop', 'open_tuesday_next')
    op.drop_column('pol_shop', 'open_wednesday_next')
    op.drop_column('pol_shop', 'open_thursday_next')
    op.drop_column('pol_shop', 'open_friday_next')
    op.drop_column('pol_shop', 'open_saturday_next')
