from uuid import UUID

from fastapi_users import BaseUserManager, UUIDIDMixin
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.daos import user
from easy_booking.exceptions.user import UserNotFound
from easy_booking.models.user import User
from easy_booking.schemas.page import Page
from easy_booking.schemas.user import UserCreate, UserOut, UserRead
from easy_booking.settings import settings


class UserService(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = settings.secret_key.get_secret_value()
    verification_token_secret = settings.secret_key.get_secret_value()

    @staticmethod
    async def add_user(user_data: UserCreate, session: AsyncSession):
        dao = user.UserDao(session)
        new_user = await dao.create(user_data)
        logger.info(f"New user created: {new_user}")
        return new_user

    @staticmethod
    async def get_all(offset: int, limit: int, session: AsyncSession) -> Page[UserRead]:
        dao = user.UserDao(session)
        users = await dao.get_all(offset=offset, limit=limit)
        return Page(
            total=await dao.count(),
            items=[UserRead.model_validate(u) for u in users],
            offset=offset,
            limit=limit,
        )

    @staticmethod
    async def delete_all(session: AsyncSession):
        await user.UserDao(session).delete_all()
        return []

    @staticmethod
    async def get_user_by_id(user_id: UUID, session: AsyncSession) -> UserRead:
        _user = await user.UserDao(session).get_by_id(user_id)
        if not _user:
            raise UserNotFound
        return _user

    @staticmethod
    async def update_by_id(user_id: UUID, user_patch: UserCreate, session: AsyncSession) -> UserRead:
        _user = await user.UserDao(session).get_by_id(user_id)
        if not _user:
            raise UserNotFound
        for key, value in user_patch.model_dump(exclude_unset=True).items():
            setattr(_user, key, value)
        await session.commit()
        return _user

    @staticmethod
    async def delete_by_id(user_id: UUID, session: AsyncSession) -> UserOut:
        _user = await user.UserDao(session).get_by_id(user_id)
        if not _user:
            raise UserNotFound
        await session.delete(_user)
        await session.commit()
        return _user