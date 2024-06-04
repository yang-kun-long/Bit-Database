"""Initial migration

Revision ID: ea72d04a0ef8
Revises: 8042dd93d857
Create Date: 2024-06-04 23:42:22.295331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea72d04a0ef8'
down_revision = '8042dd93d857'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resource_downloads', schema=None) as batch_op:
        batch_op.add_column(sa.Column('introduction', sa.Text(), nullable=True))
        batch_op.alter_column('author',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resource_downloads', schema=None) as batch_op:
        batch_op.alter_column('author',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.drop_column('introduction')

    # ### end Alembic commands ###