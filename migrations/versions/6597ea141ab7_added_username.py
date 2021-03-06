"""added username

Revision ID: 6597ea141ab7
Revises: c09f270603e4
Create Date: 2021-08-22 15:27:44.250953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6597ea141ab7'
down_revision = 'c09f270603e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(length=20), nullable=False))
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###
