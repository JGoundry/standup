"""empty message

Revision ID: fc78a207a629
Revises: 3932d3cbc849
Create Date: 2022-12-13 18:33:39.083224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc78a207a629'
down_revision = '3932d3cbc849'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('op', sa.String(length=50), nullable=True),
    sa.Column('caption', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['op'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bio', sa.String(length=150), nullable=True))
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.drop_column('bio')

    op.drop_table('post')
    # ### end Alembic commands ###
