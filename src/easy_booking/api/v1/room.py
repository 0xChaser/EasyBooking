from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.db import get_session
from easy_booking.schemas.room import (
    RoomIn,
    RoomOut,
    RoomPatch
)
from easy_booking.schemas.page import Page
from easy_booking.services.room import RoomService

router = APIRouter(prefix="/room", tags=["Room"])

@router.get("/", response_model=Page[RoomOut])
async def list_room(
    offset:int=0,
    limit:int=10,
    session:AsyncSession = Depends(get_session)
):
    """
    Get all room:
    
    Return : 
    
    RoomOut : Room with all it's attributes
    
    """
    return await RoomService.get_all_room(session=session, offset=offset, limit=limit)

@router.get("/{id}", response_model=RoomOut)
async def get_room(id:UUID, session:AsyncSession=Depends(get_session)):
    return await RoomService.get_by_id(id, session)

@router.post("/")
async def add_room(room_data:RoomIn, session:AsyncSession=Depends(get_session)):
    return await RoomService.add_room(room_data, session)

@router.patch("/{id}", response_model=RoomOut)
async def update_room(id:UUID, room:RoomPatch, session:AsyncSession=Depends(get_session)):
    return await RoomService.update_by_id(id, room, session)

@router.delete("/{id}", response_model=RoomOut)
async def delete_room(id:UUID,session:AsyncSession=Depends(get_session)):
    return await RoomService.delete_by_id(id, session)

@router.delete("/")
async def delete_all_room(session:AsyncSession=Depends(get_session)):
    return await RoomService.delete_all(session)