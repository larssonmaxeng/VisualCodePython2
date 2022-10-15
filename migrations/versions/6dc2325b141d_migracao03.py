"""Migracao03

Revision ID: 6dc2325b141d
Revises: da57a143bbe7
Create Date: 2022-10-15 08:40:28.233126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dc2325b141d'
down_revision = 'da57a143bbe7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('PacotesDeEntrega', sa.Column('preco', sa.Float(), nullable=True))
    op.add_column('PacotesDeEntrega', sa.Column('alturaMaxima', sa.Float(), nullable=True))
    op.add_column('PacotesDeEntrega', sa.Column('areaBaseMaxima', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('PacotesDeEntrega', 'areaBaseMaxima')
    op.drop_column('PacotesDeEntrega', 'alturaMaxima')
    op.drop_column('PacotesDeEntrega', 'preco')
    # ### end Alembic commands ###
