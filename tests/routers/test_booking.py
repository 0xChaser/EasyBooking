import uuid
from datetime import datetime, timedelta, timezone

import pytest

from easy_booking.daos.booking import BookingDao
from easy_booking.daos.room import RoomDao
from easy_booking.daos.user import UserDao
from easy_booking.schemas.booking import BookingIn
from easy_booking.services.booking import BookingService
from easy_booking.services.room import RoomService
from tests.utils.fake_data_generator import FakeDataGenerator


@pytest.mark.asyncio
class TestBookingRouter:

    async def test_get_all_booking(self, test_session, test_client):
        await BookingService.delete_all(test_session)
        
        user_dao = UserDao(test_session)
        room_dao = RoomDao(test_session)
        
        fake_user_data = FakeDataGenerator.fake_user()
        fake_room_data = FakeDataGenerator.fake_room()
        
        created_user = await user_dao.create(fake_user_data)
        created_room = await room_dao.create(fake_room_data)

        created_bookings = []

        for i in range(3):
            fake_booking_in = FakeDataGenerator.fake_booking_in(
                override={
                    "room_id": created_room.id,
                    "start_time": datetime.now(timezone.utc) + timedelta(days=i),
                    "end_time": datetime.now(timezone.utc) + timedelta(days=i, hours=2)
                }
            )
            created_booking = await BookingService.add_booking(
                fake_booking_in, 
                test_session, 
                created_user.id
            )
            created_bookings.append(created_booking)

        response = await test_client.get("/booking/?offset=0&limit=10")

        assert response.status_code == 200
        page_result = response.json()

        assert page_result["total"] == 3
        assert len(page_result["items"]) == 3
        assert page_result["offset"] == 0
        assert page_result["limit"] == 10

        booking_ids = [booking["id"] for booking in page_result["items"]]
        for booking in created_bookings:
            assert str(booking.id) in booking_ids

        await BookingService.delete_all(test_session)

    async def test_get_booking_by_id(self, test_session, test_client):
        user_dao = UserDao(test_session)
        room_dao = RoomDao(test_session)
        
        fake_user_data = FakeDataGenerator.fake_user()
        fake_room_data = FakeDataGenerator.fake_room()
        
        created_user = await user_dao.create(fake_user_data)
        created_room = await room_dao.create(fake_room_data)
        
        fake_booking_in = FakeDataGenerator.fake_booking_in(
            override={"room_id": created_room.id}
        )
        created_booking = await BookingService.add_booking(
            fake_booking_in, 
            test_session, 
            created_user.id
        )

        response = await test_client.get(f"/booking/{created_booking.id}")

        assert response.status_code == 200
        retrieved_booking = response.json()

        assert retrieved_booking is not None
        assert retrieved_booking["id"] == str(created_booking.id)
        assert retrieved_booking["user_id"] == str(created_user.id)
        assert retrieved_booking["room_id"] == str(created_room.id)
        assert retrieved_booking["user"] is not None
        assert retrieved_booking["room"] is not None

        await BookingDao(test_session).delete_by_id(created_booking.id)

    async def test_delete_booking_by_id(self, test_session, test_client):
        user_dao = UserDao(test_session)
        room_dao = RoomDao(test_session)
        
        fake_user_data = FakeDataGenerator.fake_user()
        fake_room_data = FakeDataGenerator.fake_room()
        
        created_user = await user_dao.create(fake_user_data)
        created_room = await room_dao.create(fake_room_data)
        
        fake_booking_in = FakeDataGenerator.fake_booking_in(
            override={"room_id": created_room.id}
        )
        created_booking = await BookingService.add_booking(
            fake_booking_in, 
            test_session, 
            created_user.id
        )

        response = await test_client.delete(f"/booking/{created_booking.id}")

        assert response.status_code == 200
        deleted_booking = response.json()

        assert deleted_booking is not None
        assert deleted_booking["id"] == str(created_booking.id)

        assert await BookingDao(test_session).get_by_id(created_booking.id) is None

    async def test_patch_booking_by_id(self, test_session, test_client):
        user_dao = UserDao(test_session)
        room_dao = RoomDao(test_session)
        
        fake_user_data = FakeDataGenerator.fake_user()
        fake_room_data = FakeDataGenerator.fake_room()
        
        created_user = await user_dao.create(fake_user_data)
        created_room = await room_dao.create(fake_room_data)
        
        fake_booking_in = FakeDataGenerator.fake_booking_in(
            override={"room_id": created_room.id}
        )
        created_booking = await BookingService.add_booking(
            fake_booking_in, 
            test_session, 
            created_user.id
        )

        new_start_time = datetime.now(timezone.utc) + timedelta(days=1)
        new_end_time = new_start_time + timedelta(hours=2)
        
        patch_data = {
            "room_id": str(created_room.id),
            "start_time": new_start_time.isoformat(),
            "end_time": new_end_time.isoformat(),
        }

        response = await test_client.patch(f"/booking/{created_booking.id}", json=patch_data)

        assert response.status_code == 200
        updated_booking = response.json()

        assert updated_booking is not None
        assert updated_booking["room_id"] == str(created_room.id)
        assert updated_booking["user"] is not None
        assert updated_booking["room"] is not None

        await BookingDao(test_session).delete_by_id(created_booking.id)

    async def test_get_booking_by_id_not_found(self, test_client):
        non_existent_id = str(uuid.uuid4())

        response = await test_client.get(f"/booking/{non_existent_id}")

        assert response.status_code == 404

    async def test_delete_booking_by_id_not_found(self, test_client):
        non_existent_id = str(uuid.uuid4())

        response = await test_client.delete(f"/booking/{non_existent_id}")

        assert response.status_code == 404

    async def test_patch_booking_by_id_not_found(self, test_client):
        non_existent_id = str(uuid.uuid4())
        start_time = datetime.now(timezone.utc)
        patch_data = {
            "room_id": str(uuid.uuid4()),
            "start_time": start_time.isoformat(),
            "end_time": (start_time + timedelta(hours=2)).isoformat(),
        }

        response = await test_client.patch(f"/booking/{non_existent_id}", json=patch_data)

        assert response.status_code == 404

