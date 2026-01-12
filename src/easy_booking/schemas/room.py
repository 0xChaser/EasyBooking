from uuid import UUID
from pydantic import BaseModel, ConfigDict


class RoomBase(BaseModel):
    name: str
    address: str
    capacity: int

    model_config = ConfigDict(from_attributes=True)


class RoomIn(RoomBase):
    description: str | None = None


class RoomOut(RoomIn):
    id: UUID


class RoomPatch(RoomIn):
    pass

