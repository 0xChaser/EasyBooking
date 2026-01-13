"""add status to room and booking

Revision ID: add_status_fields
Revises: 1b36bf5f93a5
Create Date: 2026-01-13 10:22:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'add_status_fields'
down_revision: Union[str, None] = '1b36bf5f93a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    room_status_enum = sa.Enum('available', 'unavailable', 'maintenance', name='roomstatus')
    room_status_enum.create(op.get_bind(), checkfirst=True)
    
    op.add_column('rooms', sa.Column('status', room_status_enum, nullable=False, server_default='available'))
    
    booking_status_enum = sa.Enum('scheduled', 'confirmed', 'cancelled', 'completed', name='bookingstatus')
    booking_status_enum.create(op.get_bind(), checkfirst=True)
    
    op.add_column('bookings', sa.Column('status', booking_status_enum, nullable=False, server_default='scheduled'))


def downgrade() -> None:
    op.drop_column('bookings', 'status')
    op.drop_column('rooms', 'status')
    
    sa.Enum(name='bookingstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='roomstatus').drop(op.get_bind(), checkfirst=True)
