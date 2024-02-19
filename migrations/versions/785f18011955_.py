"""empty message

Revision ID: 785f18011955
Revises: ffc598723843
Create Date: 2024-01-31 22:36:28.343267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '785f18011955'
down_revision = 'ffc598723843'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index('email', ['email'], unique=False)

    # ### end Alembic commands ###
