from uuid import UUID
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict

from easy_booking.schemas.room import RoomOut
from easy_booking.schemas.user import UserOut


class BookingStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class BookingBase(BaseModel):
    room_id: UUID
    start_time: datetime
    end_time: datetime

    model_config = ConfigDict(from_attributes=True)


class BookingIn(BookingBase):
    status: BookingStatus = BookingStatus.SCHEDULED


class BookingOut(BookingBase):
    id: UUID
    user_id: UUID
    status: BookingStatus
    created_at: datetime
    user: UserOut | None = None
    room: RoomOut | None = None


class BookingPatch(BaseModel):
    room_id: UUID | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: BookingStatus | None = None

    model_config = ConfigDict(from_attributes=True)

