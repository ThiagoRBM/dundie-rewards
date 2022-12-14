"""Adiciona o campo currency em Person

Revision ID: 79931daf04e7
Revises: 83e3ab336abd
Create Date: 2022-09-28 11:24:36.289102

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '79931daf04e7'
down_revision = '83e3ab336abd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('person', sa.Column('currency', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('person', 'currency')
    # ### end Alembic commands ###
