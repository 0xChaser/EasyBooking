from uuid import UUID

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from easy_booking.auth.auth import auth_backend
from easy_booking.dependencies import get_user_service
from easy_booking.models.user import User
from easy_booking.schemas.user import UserCreate, UserRead

fastapi_users = FastAPIUsers[User, UUID](
    get_user_service,
    [auth_backend],
)
router = APIRouter(prefix="/auth", tags=["Auth"])

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["Auth"],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["Auth"],
)