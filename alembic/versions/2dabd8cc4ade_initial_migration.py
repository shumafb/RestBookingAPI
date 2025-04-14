"""initial migration

Revision ID: 2dabd8cc4ade
Revises: 
Create Date: 2025-04-14 10:21:16.806063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2dabd8cc4ade'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tables',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('seats', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tables_id'), 'tables', ['id'], unique=False)
    op.create_table('reservations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_name', sa.String(length=50), nullable=True),
    sa.Column('table_id', sa.Integer(), nullable=True),
    sa.Column('reservation_time', sa.DateTime(), nullable=True),
    sa.Column('duration_minutes', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['table_id'], ['tables.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reservations_customer_name'), 'reservations', ['customer_name'], unique=False)
    op.create_index(op.f('ix_reservations_id'), 'reservations', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reservations_id'), table_name='reservations')
    op.drop_index(op.f('ix_reservations_customer_name'), table_name='reservations')
    op.drop_table('reservations')
    op.drop_index(op.f('ix_tables_id'), table_name='tables')
    op.drop_table('tables')
    # ### end Alembic commands ###
