"""empty message

Revision ID: d6f4b8607c31
Revises: cc7530bb47ae
Create Date: 2023-01-24 16:53:04.661912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6f4b8607c31'
down_revision = 'cc7530bb47ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=200), server_default='', nullable=False))
        batch_op.add_column(sa.Column('body', sa.Text(), server_default='', nullable=False))
        batch_op.add_column(sa.Column('dt_created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('dt_updated', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.drop_column('dt_updated')
        batch_op.drop_column('dt_created')
        batch_op.drop_column('body')
        batch_op.drop_column('title')

    # ### end Alembic commands ###
