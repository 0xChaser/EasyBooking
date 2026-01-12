"""
UserDao.
"""

from uuid import UUID

import sqlalchemy.sql.functions
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.daos.base import BaseDao
from easy_booking.exceptions.base import INVALIDDATATYPE
from easy_booking.exceptions.user import UserLinkedToAnotherObject
from easy_booking.models.user import User
from easy_booking.schemas.user import UserCreate


class UserDao(BaseDao):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.user_db = SQLAlchemyUserDatabase(session, User)

    async def create(self, request: UserCreate | dict) -> User:
        if isinstance(request, BaseModel):
            data = request.model_dump()
        elif isinstance(request, dict):
            data = request
        else:
            raise TypeError(INVALIDDATATYPE)

        _user = User(**data)
        self.session.add(_user)
        await self.session.commit()
        await self.session.refresh(_user)
        return _user

    async def get_by_id(self, user_id: UUID) -> User | None:
        statement = select(User).where(User.id == user_id)
        return await self.session.scalar(statement=statement)

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[User]:
        statement = select(User).offset(offset).limit(limit)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def delete_all(self) -> None:
        await self.session.execute(delete(User))
        await self.session.commit()

    async def delete_by_id(self, user_id: UUID) -> User:
        _user = await self.get_by_id(user_id=user_id)
        try:
            statement = delete(User).where(User.id == user_id)
            await self.session.execute(statement=statement)
            await self.session.commit()
        except IntegrityError as err:
            raise UserLinkedToAnotherObject from err
        return _user

    async def count(self) -> int:
        statement = select(sqlalchemy.sql.functions.count(User.id)).select_from(User)
        result = await self.session.execute(statement)
        return result.scalar_one()