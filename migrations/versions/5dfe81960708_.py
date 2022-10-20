"""empty message

Revision ID: 5dfe81960708
Revises: 8fee3fb140c0
Create Date: 2022-10-19 13:17:31.878883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5dfe81960708'
down_revision = '8fee3fb140c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('properties', sa.Column('join_time', sa.Time(), nullable=True))
    op.add_column('users', sa.Column('address', sa.String(length=128), nullable=True))
    op.add_column('users', sa.Column('city', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('state', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'state')
    op.drop_column('users', 'city')
    op.drop_column('users', 'address')
    op.drop_column('properties', 'join_time')
    # ### end Alembic commands ###