from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.daos.base import BaseDao
from easy_booking.exceptions.room import RoomLinkedToAnotherObject
from easy_booking.models.room import Room

class RoomDao(BaseDao):

    def __init__(self, session:AsyncSession):
        super().__init__(session)

    async def create(self, room_data: dict) -> Room:
        _room = Room(**room_data)
        self.session.add(_room)
        await self.session.commit()
        await self.session.refresh(_room)
        return _room
    
    async def get_by_id(self, room_id: UUID) -> Room | None:
        statement = select(Room).where(Room.id == room_id)
        return await self.session.scalar(statement=statement)

    async def get_all(self, offset:int, limit:int) -> list[Room]:
        statement = select(Room).offset(offset).limit(limit)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()
    
    async def delete_all(self) -> None:
        await self.session.execute(delete(Room))
        await self.session.commit()

    async def delete_by_id(self, room_id:UUID) -> None:
        _room = await self.get_by_id(room_id=room_id)
        try:
            statement = delete(Room).where(Room.id == room_id)
            await self.session.execute(statement=statement)
            await self.session.commit()
        except IntegrityError:
            raise RoomLinkedToAnotherObject
        return _room
    
    async def count(self) -> int:
        statement = select(func.count()).select_from(Room)
        result = await self.session.execute(statement=statement)
        return result.scalar_one()