"""Added date created to post

Revision ID: 15a7af59bc15
Revises: a91eba959c9e
Create Date: 2022-12-14 02:39:28.422669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15a7af59bc15'
down_revision = 'a91eba959c9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('no_of_likes', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('date_created')
        batch_op.drop_column('no_of_likes')
        batch_op.drop_column('title')

    # ### end Alembic commands ###
