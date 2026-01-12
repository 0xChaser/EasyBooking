from fastapi import APIRouter

from easy_booking.api.v1.room import router as RoomRouter
from easy_booking.api.v1.booking import router as BookingRouter
from easy_booking.api.v1.auth import router as AuthRouter
from easy_booking.api.v1.user import router as UserRouter

__all__ = (
    AuthRouter,
    RoomRouter,
    BookingRouter,
    UserRouter,
)


router = APIRouter()


for api_router in __all__:
    router.include_router(api_router)