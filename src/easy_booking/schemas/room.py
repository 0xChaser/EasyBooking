from uuid import UUID
from enum import Enum
from pydantic import BaseModel, ConfigDict


class RoomStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    MAINTENANCE = "maintenance"


class RoomBase(BaseModel):
    name: str
    address: str
    capacity: int

    model_config = ConfigDict(from_attributes=True)


class RoomIn(RoomBase):
    description: str | None = None
    status: RoomStatus = RoomStatus.AVAILABLE


class RoomOut(RoomIn):
    id: UUID


class RoomPatch(BaseModel):
    name: str | None = None
    address: str | None = None
    capacity: int | None = None
    description: str | None = None
    status: RoomStatus | None = None

    model_config = ConfigDict(from_attributes=True)

