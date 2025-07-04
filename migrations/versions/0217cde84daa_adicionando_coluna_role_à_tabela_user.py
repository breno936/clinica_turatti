"""Adicionando coluna role à tabela user

Revision ID: 0217cde84daa
Revises: 81f2b4c2214c
Create Date: 2025-06-08 13:21:05.651412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0217cde84daa'
down_revision = '81f2b4c2214c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=50), nullable=False))
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.BOOLEAN(), nullable=True))
        batch_op.drop_column('role')

    # ### end Alembic commands ###
