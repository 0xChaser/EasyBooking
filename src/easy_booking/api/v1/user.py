from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.api.v1.auth import fastapi_users
from easy_booking.db import get_session
from easy_booking.dependencies import get_user_service
from easy_booking.models.user import User
from easy_booking.schemas.page import Page
from easy_booking.schemas.user import UserCreate, UserRead
from easy_booking.services.user import UserService

router = APIRouter(prefix="/user", tags=["User"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
CurrentActiveUser = Annotated[User, Depends(fastapi_users.current_user(active=True))]
CurrentSuperuser = Annotated[User, Depends(fastapi_users.current_user(active=True, superuser=True))]


@router.get("/me", response_model=UserRead)
async def get_current_user(user: CurrentActiveUser):
    return user


@router.get("/", response_model=Page[UserRead])
async def get_users(
    user_service: UserServiceDep,
    _: CurrentSuperuser,
    session: SessionDep,
    offset: int = 0,
    limit: int = 10,
):
    return await user_service.get_all(offset=offset, limit=limit, session=session)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID, session: SessionDep):
    return await UserService.get_user_by_id(user_id, session)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: UUID, user: UserCreate, session: SessionDep):
    return await UserService.update_by_id(user_id, user, session)