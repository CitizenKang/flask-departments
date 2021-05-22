"""Department name added unique=True property

Revision ID: 913f7f9cda7c
Revises: 
Create Date: 2021-05-15 15:24:04.758847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '913f7f9cda7c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_department_name', table_name='department')
    op.create_index(op.f('ix_department_name'), 'department', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_department_name'), table_name='department')
    op.create_index('ix_department_name', 'department', ['name'], unique=False)
    # ### end Alembic commands ###
