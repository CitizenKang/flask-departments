"""empty message

Revision ID: 7bf836968dbd
Revises: 913f7f9cda7c
Create Date: 2021-05-17 20:32:49.224920

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7bf836968dbd'
down_revision = '913f7f9cda7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('employee', 'department_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('employee', 'department_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
