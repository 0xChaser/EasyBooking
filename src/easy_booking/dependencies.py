from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.daos.user import UserDao
from easy_booking.db import get_session
from easy_booking.services.user import UserService


async def get_user_dao(
    session: AsyncSession = Depends(get_session),
) -> AsyncGenerator[UserDao, None]:
    yield UserDao(session)


async def get_user_db(
    user_dao: UserDao = Depends(get_user_dao),
):
    yield user_dao.user_db


async def get_user_service(
    user_db=Depends(get_user_db),
) -> AsyncGenerator[UserService, None]:
    yield UserService(user_db)