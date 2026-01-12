from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from easy_booking.schemas.room import RoomOut
from easy_booking.schemas.user import UserOut


class BookingBase(BaseModel):
    room_id: UUID
    start_time: datetime
    end_time: datetime

    model_config = ConfigDict(from_attributes=True)


class BookingIn(BookingBase):
    pass


class BookingOut(BookingIn):
    id: UUID
    user_id: UUID
    created_at: datetime
    user: UserOut | None = None
    room: RoomOut | None = None


class BookingPatch(BookingIn):
    pass

