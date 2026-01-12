import uuid

from sqlalchemy import UUID, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from easy_booking.models.base import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=False, primary_key=True
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    address: Mapped[str] = mapped_column(String(), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer(), nullable=False)
    
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="room")

