from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.api.v1.auth import fastapi_users
from easy_booking.db import get_session
from easy_booking.models.user import User
from easy_booking.schemas.booking import (
    BookingIn,
    BookingOut,
    BookingPatch
)
from easy_booking.schemas.page import Page
from easy_booking.services.booking import BookingService

router = APIRouter(prefix="/booking", tags=["Booking"])

# Dependency to get current user
current_active_user = fastapi_users.current_user(active=True)

@router.get("/", response_model=Page[BookingOut])
async def list_booking(
    offset:int=0,
    limit:int=10,
    session:AsyncSession = Depends(get_session)
):
    """
    Get all booking:
    
    Return : 
    
    BookingOut : Booking with all it's attributes 
    
    """
    return await BookingService.get_all_booking(session=session, offset=offset, limit=limit)

@router.get("/{id}", response_model=BookingOut)
async def get_booking(id:UUID, session:AsyncSession=Depends(get_session)):
    return await BookingService.get_by_id(id, session)

@router.post("/")
async def add_booking(
    booking_data:BookingIn, 
    session:AsyncSession=Depends(get_session),
    user: User = Depends(current_active_user)
):
    return await BookingService.add_booking(booking_data, session, user.id)

@router.patch("/{id}", response_model=BookingOut)
async def update_booking(id:UUID, booking:BookingPatch, session:AsyncSession=Depends(get_session)):
    return await BookingService.update_by_id(id, booking, session)

@router.delete("/{id}", response_model=BookingOut)
async def delete_booking(id:UUID,session:AsyncSession=Depends(get_session)):
    return await BookingService.delete_by_id(id, session)

@router.delete("/")
async def delete_all_booking(session:AsyncSession=Depends(get_session)):
    return await BookingService.delete_all(session)