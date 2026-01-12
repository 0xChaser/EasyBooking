from datetime import datetime
from uuid import UUID

from fastapi_users import schemas
from pydantic import BaseModel

from easy_booking.utils import optional


class UserRead(schemas.BaseUser[UUID]):
    first_name: str
    last_name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):

    first_name: str
    last_name: str
    email: str
    password: str


class UserUpdate(schemas.BaseUserUpdate):

    email: str | None = None
    password: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None


class UserOut(BaseModel):

    id: UUID
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


@optional
class UserPatch(UserCreate):
    pass