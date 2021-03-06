"""empty message

Revision ID: 3eed35c0723b
Revises:
Create Date: 2019-07-04 13:56:15.388410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3eed35c0723b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
	# ### commands auto generated by Alembic - please adjust! ###
	op.create_table(
		'users',
		sa.Column('id', sa.Integer(), nullable=False),
		sa.Column('username', sa.Unicode(length=256), nullable=False),
		sa.Column('password', sa.String(length=128), nullable=False),
		sa.PrimaryKeyConstraint('id')
	)
	op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
	# ### end Alembic commands ###


def downgrade():
	# ### commands auto generated by Alembic - please adjust! ###
	op.drop_index(op.f('ix_users_username'), table_name='users')
	op.drop_table('users')
	# ### end Alembic commands ###
