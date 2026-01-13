from uuid import UUID

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.daos import booking, room
from easy_booking.exceptions.booking import BookingNotFound
from easy_booking.exceptions.room import RoomNotFound, RoomUnavailable
from easy_booking.models.room import RoomStatus
from easy_booking.schemas.booking import BookingIn, BookingOut, BookingPatch
from easy_booking.schemas.page import Page


class BookingService:

    @staticmethod
    async def add_booking(booking_data:BookingIn, session:AsyncSession, user_id:UUID):
        room_dao = room.RoomDao(session)
        _room = await room_dao.get_by_id(booking_data.room_id)
        if not _room:
            raise RoomNotFound
        if _room.status != RoomStatus.AVAILABLE:
            raise RoomUnavailable(_room.status.value)
        
        if await booking.BookingDao(session).check_overlapping_bookings(booking_data.room_id, booking_data.start_time, booking_data.end_time):
             raise RoomUnavailable("Room is already booked for this time period")
        
        booking_dict = booking_data.model_dump()
        booking_dict["user_id"] = user_id
        new_booking = await booking.BookingDao(session).create(booking_dict)
        logger.info(f"New booking created successfully: {new_booking}")
        return new_booking
    
    @staticmethod
    async def get_all_booking(offset:int, limit:int, session:AsyncSession) -> Page[BookingOut]:
        all_booking = await booking.BookingDao(session).get_all(offset=offset, limit=limit)
        return Page(
            total = await booking.BookingDao(session).count(),
            items=[BookingOut.model_validate(_booking) for _booking in all_booking],
            offset=offset,
            limit=limit,
        )
    
    @staticmethod
    async def get_by_id(booking_id:UUID, session:AsyncSession) -> BookingOut | None :
        _booking = await booking.BookingDao(session).get_by_id(booking_id)
        if not _booking:
            raise BookingNotFound
        return _booking
    
    @staticmethod
    async def update_by_id(booking_id: UUID, booking_patch:BookingPatch, session:AsyncSession) -> BookingPatch:
        _booking = await booking.BookingDao(session).get_by_id(booking_id)
        if not _booking:
            raise BookingNotFound
        for key,value in booking_patch.model_dump(exclude_unset=True).items():
            setattr(_booking, key, value)
        await session.commit()
        _booking = await booking.BookingDao(session).get_by_id(booking_id)
        return _booking
    
    @staticmethod
    async def delete_by_id(booking_id:UUID, session:AsyncSession) -> None:
        _booking = await booking.BookingDao(session).delete_by_id(booking_id)
        if not _booking:
            raise BookingNotFound
        return _booking
    
    @staticmethod
    async def delete_all(session:AsyncSession) -> None:
        await booking.BookingDao(session).delete_all()
        return []