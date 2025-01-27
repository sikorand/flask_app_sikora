"""add is_active, category

Revision ID: f02786df9842
Revises: d0ee2d4948b3
Create Date: 2025-01-17 23:43:24.306914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f02786df9842'
down_revision = 'd0ee2d4948b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('category', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('author', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('author')
        batch_op.drop_column('category')
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###