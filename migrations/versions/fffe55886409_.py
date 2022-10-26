"""empty message

Revision ID: fffe55886409
Revises: a2061d91d743
Create Date: 2022-10-25 11:10:15.700651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fffe55886409'
down_revision = 'a2061d91d743'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(length=128), nullable=True))
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.drop_column('users', 'password')
    # ### end Alembic commands ###
