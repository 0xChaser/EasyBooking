from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from easy_booking.daos.base import BaseDao
from easy_booking.exceptions.booking import BookingLinkedToAnotherObject
from easy_booking.exceptions.booking import BookingLinkedToAnotherObject
from easy_booking.models.booking import Booking, BookingStatus

class BookingDao(BaseDao):
    def __init__(self, session:AsyncSession):
        super().__init__(session)

    async def create(self, booking_data: dict) -> Booking:
        _booking = Booking(**booking_data)
        self.session.add(_booking)
        await self.session.commit()
        await self.session.refresh(_booking)
        booking_id = _booking.id
        statement = (
            select(Booking)
            .where(Booking.id == booking_id)
            .options(selectinload(Booking.user), selectinload(Booking.room))
        )
        _booking = await self.session.scalar(statement=statement)
        return _booking
    
    async def get_by_id(self, booking_id: UUID) -> Booking | None:
        statement = (
            select(Booking)
            .where(Booking.id == booking_id)
            .options(selectinload(Booking.user), selectinload(Booking.room))
        )
        return await self.session.scalar(statement=statement)

    async def get_all(self, offset:int, limit:int, user_id: UUID | None = None) -> list[Booking]:
        statement = (
            select(Booking)
            .offset(offset)
            .limit(limit)
            .options(selectinload(Booking.user), selectinload(Booking.room))
        )
        if user_id:
            statement = statement.where(Booking.user_id == user_id)
        
        result = await self.session.execute(statement=statement)
        return result.scalars().all()
    
    async def delete_all(self) -> None:
        await self.session.execute(delete(Booking))
        await self.session.commit()

    async def delete_by_id(self, booking_id:UUID) -> None:
        _booking = await self.get_by_id(booking_id=booking_id)
        try:
            statement = delete(Booking).where(Booking.id == booking_id)
            await self.session.execute(statement=statement)
            await self.session.commit()
        except IntegrityError:
            raise BookingLinkedToAnotherObject
        return _booking
    
    async def count(self, user_id: UUID | None = None) -> int:
        statement = select(func.count()).select_from(Booking)
        if user_id:
            statement = statement.where(Booking.user_id == user_id)
        result = await self.session.execute(statement=statement)
        return result.scalar_one()

    async def check_overlapping_bookings(self, room_id: UUID, start_time: datetime, end_time: datetime) -> bool:
        statement = select(Booking).where(
            Booking.room_id == room_id,
            Booking.start_time < end_time,
            Booking.end_time > start_time,
            Booking.status != BookingStatus.CANCELLED
        )
        result = await self.session.execute(statement)
        return result.scalars().first() is not None