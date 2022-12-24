"""add phones table

Revision ID: c3f5ee51d614
Revises: 645bb9be7001
Create Date: 2022-12-22 22:36:42.713485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3f5ee51d614'
down_revision = '645bb9be7001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('phones',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cell_phone', sa.String(length=100), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('phones')
    # ### end Alembic commands ###
