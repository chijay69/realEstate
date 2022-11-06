"""empty message

Revision ID: 77bd01c5744d
Revises: d3cd7b57b216
Create Date: 2022-10-31 21:06:37.732981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77bd01c5744d'
down_revision = 'd3cd7b57b216'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('credit_cards', sa.Column('card_password', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('credit_cards', 'card_password')
    # ### end Alembic commands ###
