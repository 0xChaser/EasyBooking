import random
import uuid
from datetime import datetime, timedelta, timezone

from faker import Faker

from easy_booking.schemas.booking import BookingIn, BookingOut
from easy_booking.schemas.room import RoomIn, RoomOut
from easy_booking.schemas.user import UserCreate

fake = Faker("fr_FR")


class FakeDataGenerator:
    @staticmethod
    def fake_user(override: UserCreate | dict | None = None) -> dict:
        data = {
            "id": uuid.uuid4(),
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "hashed_password": "hashed_" + fake.password(),
            "is_active": True,
            "is_superuser": False,
            "is_verified": True,
            "created_at": datetime.now(timezone.utc),
        }
        if override:
            if isinstance(override, UserCreate):
                data.update(override.model_dump())
            else:
                data.update(override)
        return data


    @staticmethod
    def fake_user_create(override: dict | None = None) -> UserCreate:
        data = {
            "email": fake.email(),
            "hashed_password": "hashed_" + fake.password(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        }
        if override:
            data.update(override)
        return UserCreate(**data)


    @staticmethod
    def fake_room(override: RoomIn | dict | None = None) -> dict:
        data = {
            "id": uuid.uuid4(),
            "name": fake.company() + " Room",
            "address": fake.address(),
            "capacity": random.randint(1, 50),
            "description": fake.text(max_nb_chars=200),
        }
        if override:
            if isinstance(override, RoomIn):
                data.update(override.model_dump())
            else:
                data.update(override)
        return data

    @staticmethod
    def fake_room_out(override: RoomIn | dict | None = None) -> RoomOut:
        data = {
            "id": uuid.uuid4(),
            "name": fake.company() + " Room",
            "address": fake.address(),
            "capacity": random.randint(1, 50),
            "description": fake.text(max_nb_chars=200),
        }
        if override:
            if isinstance(override, RoomIn):
                data.update(override.model_dump())
            else:
                data.update(override)
        return RoomOut(**data)

    @staticmethod
    def fake_room_in(override: dict | None = None) -> RoomIn:
        data = {
            "name": fake.company() + " Room",
            "address": fake.address(),
            "capacity": random.randint(1, 50),
            "description": fake.text(max_nb_chars=200),
        }
        if override:
            data.update(override)
        return RoomIn(**data)

    @staticmethod
    def fake_booking(override: BookingIn | dict | None = None) -> dict:
        start_time = datetime.now(timezone.utc)
        data = {
            "id": uuid.uuid4(),
            "user_id": uuid.uuid4(),
            "room_id": uuid.uuid4(),
            "start_time": start_time,
            "end_time": start_time + timedelta(hours=random.randint(1, 8)),
            "created_at": datetime.now(timezone.utc),
        }
        if override:
            if isinstance(override, BookingIn):
                override_dict = override.model_dump()
            else:
                override_dict = override
            data.update(override_dict)
        return data

    @staticmethod
    def fake_booking_out(override: BookingIn | dict | None = None) -> BookingOut:
        start_time = datetime.now(timezone.utc)
        data = {
            "id": uuid.uuid4(),
            "user_id": uuid.uuid4(),
            "room_id": uuid.uuid4(),
            "start_time": start_time,
            "end_time": start_time + timedelta(hours=random.randint(1, 8)),
            "created_at": datetime.now(timezone.utc),
            "user": None,
            "room": None,
        }
        if override:
            if isinstance(override, BookingIn):
                override_dict = override.model_dump()
            else:
                override_dict = override
            data.update(override_dict)
        return BookingOut(**data)

    @staticmethod
    def fake_booking_data(
        user_id: uuid.UUID, room_id: uuid.UUID, override: dict | None = None
    ) -> dict:
        start_time = datetime.now(timezone.utc)
        data = {
            "id": uuid.uuid4(),
            "user_id": user_id,
            "room_id": room_id,
            "start_time": start_time,
            "end_time": start_time + timedelta(hours=random.randint(1, 8)),
            "created_at": datetime.now(timezone.utc),
        }
        if override:
            data.update(override)
        return data

    @staticmethod
    def fake_booking_in(override: dict | None = None) -> BookingIn:
        start_time = datetime.now(timezone.utc)
        data = {
            "room_id": uuid.uuid4(),
            "start_time": start_time,
            "end_time": start_time + timedelta(hours=random.randint(1, 8)),
        }
        if override:
            data.update(override)
        return BookingIn(**data)