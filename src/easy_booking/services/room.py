from uuid import UUID

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.daos import room
from easy_booking.exceptions.room import RoomNotFound
from easy_booking.schemas.room import RoomIn, RoomOut, RoomPatch
from easy_booking.schemas.page import Page


class RoomService:

    @staticmethod
    async def add_room(room_data:RoomIn, session:AsyncSession):
        new_room = await room.RoomDao(session).create(room_data.model_dump())
        logger.info(f"New room created successfully: {new_room}")
        return new_room
    
    @staticmethod
    async def get_all_room(offset:int, limit:int, session:AsyncSession) -> Page[RoomOut]:
        all_room = await room.RoomDao(session).get_all(offset=offset, limit=limit)
        return Page(
            total = await room.RoomDao(session).count(),
            items=[RoomOut.model_validate(_room) for _room in all_room],
            offset=offset,
            limit=limit,
        )
    
    @staticmethod
    async def get_by_id(room_id:UUID, session:AsyncSession) -> RoomOut | None :
        _room = await room.RoomDao(session).get_by_id(room_id)
        if not _room:
            raise RoomNotFound
        return _room
    
    @staticmethod
    async def update_by_id(room_id: UUID, room_patch:RoomPatch, session:AsyncSession) -> RoomPatch:
        _room = await room.RoomDao(session).get_by_id(room_id)
        if not _room:
            raise RoomNotFound
        for key,value in room_patch.model_dump(exclude_unset=True).items():
            setattr(_room, key, value)
        await session.commit()
        return _room
    
    @staticmethod
    async def delete_by_id(room_id:UUID, session:AsyncSession) -> None:
        _room = await room.RoomDao(session).delete_by_id(room_id)
        if not _room:
            raise RoomNotFound
        return _room
    
    @staticmethod
    async def delete_all(session:AsyncSession) -> None:
        await room.RoomDao(session).delete_all()
        return []