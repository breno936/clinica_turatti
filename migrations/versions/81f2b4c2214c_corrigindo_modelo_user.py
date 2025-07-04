"""Corrigindo modelo User

Revision ID: 81f2b4c2214c
Revises: 
Create Date: 2025-06-08 10:37:22.727562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81f2b4c2214c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=150), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('consulta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_hora', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('paciente_id', sa.Integer(), nullable=False),
    sa.Column('medico_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['medico_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['paciente_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('consulta')
    op.drop_table('user')
    # ### end Alembic commands ###
