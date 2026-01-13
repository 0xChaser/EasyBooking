import uuid
from enum import Enum

from sqlalchemy import UUID, String, Integer, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from easy_booking.models.base import Base


class RoomStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    MAINTENANCE = "maintenance"


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=False, primary_key=True
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    address: Mapped[str] = mapped_column(String(), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer(), nullable=False)
    status: Mapped[RoomStatus] = mapped_column(
        SQLEnum(RoomStatus, values_callable=lambda x: [e.value for e in x]), default=RoomStatus.AVAILABLE, nullable=False
    )
    
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="room")

