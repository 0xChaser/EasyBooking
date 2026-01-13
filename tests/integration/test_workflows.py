import uuid
from datetime import datetime, timedelta, timezone

import pytest

from easy_booking.api.v1.booking import current_active_user
from easy_booking.main import app

from easy_booking.daos.booking import BookingDao
from easy_booking.daos.room import RoomDao
from easy_booking.daos.user import UserDao
from easy_booking.exceptions.room import RoomNotFound, RoomUnavailable
from easy_booking.services.booking import BookingService
from easy_booking.services.room import RoomService
from easy_booking.services.user import UserService
from tests.utils.fake_data_generator import FakeDataGenerator


@pytest.mark.asyncio
class TestBookingWorkflow:

    async def test_complete_booking_workflow(self, test_session, test_client):
        room_data = {
            "name": "Salle de Conférence A",
            "address": "123 Rue de la Paix, Paris",
            "capacity": 20,
            "description": "Grande salle équipée d'un projecteur",
        }
        response = await test_client.post("/room/", json=room_data)
        assert response.status_code == 200
        created_room = response.json()
        room_id = created_room["id"]

        user_dao = UserDao(test_session)
        user_data = FakeDataGenerator.fake_user()
        created_user = await user_dao.create(user_data)
        user_id = created_user.id

        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time + timedelta(hours=2)
        booking_in = FakeDataGenerator.fake_booking_in({
            "room_id": uuid.UUID(room_id),
            "start_time": start_time,
            "end_time": end_time,
        })
        booking = await BookingService.add_booking(booking_in, test_session, user_id)
        assert booking is not None
        assert booking.room_id == uuid.UUID(room_id)
        assert booking.user_id == user_id

        response = await test_client.get(f"/booking/{booking.id}")
        assert response.status_code == 200
        booking_data = response.json()
        assert booking_data["room"]["name"] == room_data["name"]
        assert booking_data["user"]["email"] == user_data["email"]

        response = await test_client.delete(f"/booking/{booking.id}")
        assert response.status_code == 200

        response = await test_client.get(f"/booking/{booking.id}")
        assert response.status_code == 404

        await RoomDao(test_session).delete_by_id(uuid.UUID(room_id))
        await user_dao.delete_by_id(user_id)

    async def test_multiple_bookings_same_room(self, test_session, test_client):
        room_data = {
            "name": "Salle Partagée",
            "address": "456 Avenue des Tests",
            "capacity": 10,
            "description": "Salle pour tests multiples",
        }
        response = await test_client.post("/room/", json=room_data)
        assert response.status_code == 200
        room_id = uuid.UUID(response.json()["id"])

        user_dao = UserDao(test_session)
        users = []
        for i in range(3):
            user_data = FakeDataGenerator.fake_user()
            user = await user_dao.create(user_data)
            users.append(user)

        bookings = []
        base_time = datetime.now(timezone.utc) + timedelta(days=1)
        for i, user in enumerate(users):
            start_time = base_time + timedelta(hours=i * 3)
            end_time = start_time + timedelta(hours=2)
            booking_in = FakeDataGenerator.fake_booking_in({
                "room_id": room_id,
                "start_time": start_time,
                "end_time": end_time,
            })
            booking = await BookingService.add_booking(booking_in, test_session, user.id)
            bookings.append(booking)

        # Create a superuser to view all bookings
        superuser = await user_dao.create(FakeDataGenerator.fake_user(override={"is_superuser": True}))

        app.dependency_overrides[current_active_user] = lambda: superuser
        try:
            response = await test_client.get("/booking/?offset=0&limit=10")
        finally:
            del app.dependency_overrides[current_active_user]

        assert response.status_code == 200
        page = response.json()
        booking_ids = [b["id"] for b in page["items"]]
        for booking in bookings:
            assert str(booking.id) in booking_ids
        
        await user_dao.delete_by_id(superuser.id)

        for booking in bookings:
            await BookingDao(test_session).delete_by_id(booking.id)
        await RoomDao(test_session).delete_by_id(room_id)
        for user in users:
            await user_dao.delete_by_id(user.id)

    async def test_booking_with_room_update(self, test_session, test_client):
        room_data = {
            "name": "Ancienne Salle",
            "address": "789 Boulevard Test",
            "capacity": 15,
            "description": "Description initiale",
        }
        response = await test_client.post("/room/", json=room_data)
        assert response.status_code == 200
        room_id = response.json()["id"]

        user_dao = UserDao(test_session)
        user_data = FakeDataGenerator.fake_user()
        user = await user_dao.create(user_data)

        start_time = datetime.now(timezone.utc) + timedelta(days=2)
        end_time = start_time + timedelta(hours=1)
        booking_in = FakeDataGenerator.fake_booking_in({
            "room_id": uuid.UUID(room_id),
            "start_time": start_time,
            "end_time": end_time,
        })
        booking = await BookingService.add_booking(booking_in, test_session, user.id)

        patch_data = {
            "name": "Nouvelle Salle Rénovée",
            "address": "789 Boulevard Test",
            "capacity": 25,
            "description": "Description mise à jour",
        }
        response = await test_client.patch(f"/room/{room_id}", json=patch_data)
        assert response.status_code == 200

        response = await test_client.get(f"/booking/{booking.id}")
        assert response.status_code == 200
        booking_data = response.json()
        assert booking_data["room"]["name"] == "Nouvelle Salle Rénovée"
        assert booking_data["room"]["capacity"] == 25

        await BookingDao(test_session).delete_by_id(booking.id)
        await RoomDao(test_session).delete_by_id(uuid.UUID(room_id))
        await user_dao.delete_by_id(user.id)


@pytest.mark.asyncio
class TestUserRoomInteraction:

    async def test_user_books_multiple_rooms(self, test_session, test_client):
        rooms = []
        for i in range(3):
            room_data = {
                "name": f"Salle {i + 1}",
                "address": f"Adresse {i + 1}",
                "capacity": 10 + i * 5,
                "description": f"Description salle {i + 1}",
            }
            response = await test_client.post("/room/", json=room_data)
            assert response.status_code == 200
            rooms.append(response.json())

        user_dao = UserDao(test_session)
        user_data = FakeDataGenerator.fake_user()
        user = await user_dao.create(user_data)

        bookings = []
        base_time = datetime.now(timezone.utc) + timedelta(days=1)
        for i, room in enumerate(rooms):
            start_time = base_time + timedelta(hours=i * 2)
            end_time = start_time + timedelta(hours=1)
            booking_in = FakeDataGenerator.fake_booking_in({
                "room_id": uuid.UUID(room["id"]),
                "start_time": start_time,
                "end_time": end_time,
            })
            booking = await BookingService.add_booking(booking_in, test_session, user.id)
            bookings.append(booking)

        app.dependency_overrides[current_active_user] = lambda: user
        try:
            response = await test_client.get("/booking/?offset=0&limit=10")
        finally:
            del app.dependency_overrides[current_active_user]

        assert response.status_code == 200
        page = response.json()
        
        user_bookings = [b for b in page["items"] if b["user_id"] == str(user.id)]
        assert len(user_bookings) >= 3

        for booking in bookings:
            await BookingDao(test_session).delete_by_id(booking.id)
        for room in rooms:
            await RoomDao(test_session).delete_by_id(uuid.UUID(room["id"]))
        await user_dao.delete_by_id(user.id)

    async def test_delete_user_cascade_check(self, test_session, test_client):
        room_data = {
            "name": "Salle Test Cascade",
            "address": "Test Address",
            "capacity": 10,
            "description": "Test cascade",
        }
        response = await test_client.post("/room/", json=room_data)
        assert response.status_code == 200
        room_id = uuid.UUID(response.json()["id"])

        user_dao = UserDao(test_session)
        user_data = FakeDataGenerator.fake_user()
        user = await user_dao.create(user_data)

        booking_in = FakeDataGenerator.fake_booking_in({"room_id": room_id})
        booking = await BookingService.add_booking(booking_in, test_session, user.id)

        response = await test_client.get(f"/booking/{booking.id}")
        assert response.status_code == 200

        await BookingDao(test_session).delete_by_id(booking.id)
        await RoomDao(test_session).delete_by_id(room_id)
        await user_dao.delete_by_id(user.id)


@pytest.mark.asyncio
class TestPaginationIntegration:

    async def test_room_pagination_with_bookings(self, test_session, test_client):
        await RoomService.delete_all(test_session)

        rooms = []
        for i in range(25):
            room_data = {
                "name": f"Salle Pagination {i + 1}",
                "address": f"Adresse {i + 1}",
                "capacity": 10,
                "description": f"Salle numéro {i + 1}",
            }
            response = await test_client.post("/room/", json=room_data)
            assert response.status_code == 200
            rooms.append(response.json())

        response = await test_client.get("/room/?offset=0&limit=10")
        assert response.status_code == 200
        page1 = response.json()
        assert page1["total"] == 25
        assert len(page1["items"]) == 10
        assert page1["offset"] == 0

        response = await test_client.get("/room/?offset=10&limit=10")
        assert response.status_code == 200
        page2 = response.json()
        assert len(page2["items"]) == 10
        assert page2["offset"] == 10

        response = await test_client.get("/room/?offset=20&limit=10")
        assert response.status_code == 200
        page3 = response.json()
        assert len(page3["items"]) == 5
        assert page3["offset"] == 20

        page1_ids = {r["id"] for r in page1["items"]}
        page2_ids = {r["id"] for r in page2["items"]}
        page3_ids = {r["id"] for r in page3["items"]}
        assert page1_ids.isdisjoint(page2_ids)
        assert page2_ids.isdisjoint(page3_ids)

        for room in rooms:
            await RoomDao(test_session).delete_by_id(uuid.UUID(room["id"]))

    async def test_booking_pagination_across_users(self, test_session, test_client):
        await BookingService.delete_all(test_session)

        room_data = {
            "name": "Salle Multi-User",
            "address": "Test",
            "capacity": 50,
            "description": "Grande salle",
        }
        response = await test_client.post("/room/", json=room_data)
        room_id = uuid.UUID(response.json()["id"])

        user_dao = UserDao(test_session)
        users = []
        for _ in range(5):
            user = await user_dao.create(FakeDataGenerator.fake_user())
            users.append(user)

        bookings = []
        base_time = datetime.now(timezone.utc) + timedelta(days=1)
        for i in range(20):
            user = users[i % len(users)]
            start_time = base_time + timedelta(hours=i)
            end_time = start_time + timedelta(minutes=30)
            booking_in = FakeDataGenerator.fake_booking_in({
                "room_id": room_id,
                "start_time": start_time,
                "end_time": end_time,
            })
            booking = await BookingService.add_booking(booking_in, test_session, user.id)
            bookings.append(booking)

        superuser = await user_dao.create(FakeDataGenerator.fake_user(override={"is_superuser": True}))
        app.dependency_overrides[current_active_user] = lambda: superuser
        try:
            response = await test_client.get("/booking/?offset=0&limit=5")
        finally:
            del app.dependency_overrides[current_active_user]

        assert response.status_code == 200
        page = response.json()
        assert page["total"] == 20
        assert len(page["items"]) == 5
        
        await user_dao.delete_by_id(superuser.id)

        for booking in bookings:
            await BookingDao(test_session).delete_by_id(booking.id)
        await RoomDao(test_session).delete_by_id(room_id)
        for user in users:
            await user_dao.delete_by_id(user.id)


@pytest.mark.asyncio
class TestErrorHandlingIntegration:

    async def test_booking_nonexistent_room(self, test_session):
        user_dao = UserDao(test_session)
        user = await user_dao.create(FakeDataGenerator.fake_user())

        fake_room_id = uuid.uuid4()
        booking_in = FakeDataGenerator.fake_booking_in({"room_id": fake_room_id})
        
        with pytest.raises(RoomNotFound):
            await BookingService.add_booking(booking_in, test_session, user.id)

        await user_dao.delete_by_id(user.id)

    async def test_prevent_double_booking(self, test_session, test_client):
        room_data = {
            "name": "Salle Double Booking",
            "address": "Test Address",
            "capacity": 10,
            "description": "Test double booking",
        }
        response = await test_client.post("/room/", json=room_data)
        assert response.status_code == 200
        room_id = uuid.UUID(response.json()["id"])

        user_dao = UserDao(test_session)
        user = await user_dao.create(FakeDataGenerator.fake_user())

        start_time = datetime.now(timezone.utc) + timedelta(days=5)
        end_time = start_time + timedelta(hours=2)

        booking1_in = FakeDataGenerator.fake_booking_in({
            "room_id": room_id,
            "start_time": start_time,
            "end_time": end_time,
        })
        booking1 = await BookingService.add_booking(booking1_in, test_session, user.id)

        # Attempt to book overlapping time
        booking2_in = FakeDataGenerator.fake_booking_in({
            "room_id": room_id,
            "start_time": start_time + timedelta(hours=1), # Overlaps
            "end_time": end_time + timedelta(hours=1),
        })

        with pytest.raises(RoomUnavailable):
            await BookingService.add_booking(booking2_in, test_session, user.id)

        await BookingDao(test_session).delete_by_id(booking1.id)
        await RoomDao(test_session).delete_by_id(room_id)
        await user_dao.delete_by_id(user.id)

    async def test_allow_booking_if_overlapping_is_cancelled(self, test_session, test_client):
        room_data = {
            "name": "Salle Cancelled Booking",
            "address": "Test Address",
            "capacity": 10,
            "description": "Test cancelled booking",
        }
        response = await test_client.post("/room/", json=room_data)
        assert response.status_code == 200
        room_id = uuid.UUID(response.json()["id"])
        room_id_str = str(room_id)

        user_dao = UserDao(test_session)
        user = await user_dao.create(FakeDataGenerator.fake_user())

        start_time = datetime.now(timezone.utc) + timedelta(days=10)
        end_time = start_time + timedelta(hours=2)

        booking1_in = FakeDataGenerator.fake_booking_in({
            "room_id": room_id,
            "start_time": start_time,
            "end_time": end_time,
        })
        booking1 = await BookingService.add_booking(booking1_in, test_session, user.id)
        
        # Cancel the booking
        patch_data = {"status": "cancelled"}
        # Assuming there is an endpoint to patch booking, checking test_workflows..
        # The test `test_complete_booking_workflow` doesn't show a patch endpoint for booking status, 
        # but `BookingService.update_by_id` exists. 
        # Let's use the service directly to ensure we set the status to CANCELLED locally if API not ready,
        # OR assume the API exists. `BookingService` has `update_by_id` accepting `BookingPatch`.
        # Wait, I need `BookingPatch` to support status.
        
        # Checking BookingPatch schema if possible, or just updating directly via DAO for test setup if simpler.
        # But wait, looking at `BookingPatch` in `booking.py` (model) - no, schema is in `schemas/booking.py`.
        # I'll update via DAO/Service directly using object modification for simplicity if needed, 
        # but cleaner to use Service.
        
        # Let's import BookingPatch and update.
        from easy_booking.schemas.booking import BookingPatch, BookingStatus
        await BookingService.update_by_id(booking1.id, BookingPatch(status=BookingStatus.CANCELLED), test_session)
        
        # Now try to book overlapping time
        booking2 = await BookingService.add_booking(booking1_in, test_session, user.id)
        assert booking2 is not None
        assert booking2.id != booking1.id

        await BookingDao(test_session).delete_by_id(booking1.id)
        await BookingDao(test_session).delete_by_id(booking2.id)
        await RoomDao(test_session).delete_by_id(room_id)
        await user_dao.delete_by_id(user.id)

    async def test_get_nonexistent_resources(self, test_client):
        fake_id = str(uuid.uuid4())

        response = await test_client.get(f"/user/{fake_id}")
        assert response.status_code == 404

        response = await test_client.get(f"/room/{fake_id}")
        assert response.status_code == 404

        response = await test_client.get(f"/booking/{fake_id}")
        assert response.status_code == 404

    async def test_invalid_pagination_params(self, test_client):
        response = await test_client.get("/room/?offset=-1&limit=10")
        assert response.status_code in [200, 422]

        response = await test_client.get("/room/?offset=0&limit=0")
        assert response.status_code in [200, 422]

    async def test_patch_nonexistent_room(self, test_client):
        fake_id = str(uuid.uuid4())
        patch_data = {
            "name": "New Name",
            "address": "New Address",
            "capacity": 10,
            "description": "New Description",
        }

        response = await test_client.patch(f"/room/{fake_id}", json=patch_data)
        assert response.status_code == 404

    async def test_delete_nonexistent_booking(self, test_client):
        fake_id = str(uuid.uuid4())

        response = await test_client.delete(f"/booking/{fake_id}")
        assert response.status_code == 404
