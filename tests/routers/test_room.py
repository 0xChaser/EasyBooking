import uuid

import pytest

from easy_booking.daos.room import RoomDao
from easy_booking.schemas.room import RoomIn
from easy_booking.services.room import RoomService
from tests.utils.fake_data_generator import FakeDataGenerator


@pytest.mark.asyncio
class TestRoomRouter:

    async def test_add_room(self, test_session, test_client):
        fake_room_data = FakeDataGenerator.fake_room()
        room_data = {
            "name": fake_room_data["name"],
            "address": fake_room_data["address"],
            "capacity": fake_room_data["capacity"],
            "description": fake_room_data["description"],
        }

        response = await test_client.post("/room/", json=room_data)

        assert response.status_code == 200
        created_room = response.json()
        assert created_room["id"] is not None
        assert created_room["name"] == fake_room_data["name"]
        assert created_room["address"] == fake_room_data["address"]
        assert created_room["capacity"] == fake_room_data["capacity"]
        assert created_room["description"] == fake_room_data["description"]

        room_id = uuid.UUID(created_room["id"])
        retrieved_room = await RoomDao(test_session).get_by_id(room_id)
        assert retrieved_room is not None
        assert str(retrieved_room.id) == created_room["id"]

        await RoomDao(test_session).delete_by_id(room_id)

    async def test_get_all_room(self, test_session, test_client):
        await RoomService.delete_all(test_session)

        created_rooms = []

        for _ in range(3):
            fake_room_data = FakeDataGenerator.fake_room()
            room_in = RoomIn(
                name=fake_room_data["name"],
                address=fake_room_data["address"],
                capacity=fake_room_data["capacity"],
                description=fake_room_data["description"],
            )
            created_room = await RoomService.add_room(room_in, test_session)
            created_rooms.append(created_room)

        response = await test_client.get("/room/?offset=0&limit=10")

        assert response.status_code == 200
        page_result = response.json()

        assert page_result["total"] == 3
        assert len(page_result["items"]) == 3
        assert page_result["offset"] == 0
        assert page_result["limit"] == 10

        room_ids = [room["id"] for room in page_result["items"]]
        for room in created_rooms:
            assert str(room.id) in room_ids

        await RoomService.delete_all(test_session)

    async def test_get_room_by_id(self, test_session, test_client):
        fake_room_data = FakeDataGenerator.fake_room()
        room_data = {
            "name": fake_room_data["name"],
            "address": fake_room_data["address"],
            "capacity": fake_room_data["capacity"],
            "description": fake_room_data["description"],
        }

        response = await test_client.post("/room/", json=room_data)

        assert response.status_code == 200
        created_room = response.json()

        assert created_room["id"] is not None

        response = await test_client.get(f"/room/{created_room['id']}")

        assert response.status_code == 200
        retrieved_room = response.json()

        assert retrieved_room is not None
        assert retrieved_room["name"] == room_data["name"]
        assert retrieved_room["address"] == room_data["address"]
        assert retrieved_room["capacity"] == room_data["capacity"]
        assert retrieved_room["description"] == room_data["description"]

        await RoomDao(test_session).delete_by_id(uuid.UUID(created_room["id"]))

    async def test_delete_room_by_id(self, test_session, test_client):
        fake_room_data = FakeDataGenerator.fake_room()
        room_data = {
            "name": fake_room_data["name"],
            "address": fake_room_data["address"],
            "capacity": fake_room_data["capacity"],
            "description": fake_room_data["description"],
        }

        response = await test_client.post("/room/", json=room_data)

        assert response.status_code == 200
        created_room = response.json()

        assert created_room["id"] is not None

        response = await test_client.delete(f"/room/{created_room['id']}")

        assert response.status_code == 200
        deleted_room = response.json()

        assert deleted_room is not None

        assert await RoomDao(test_session).get_by_id(uuid.UUID(created_room["id"])) is None

    async def test_patch_room_by_id(self, test_session, test_client):
        fake_room_data = FakeDataGenerator.fake_room()
        room_data = {
            "name": fake_room_data["name"],
            "address": fake_room_data["address"],
            "capacity": fake_room_data["capacity"],
            "description": fake_room_data["description"],
        }

        response = await test_client.post("/room/", json=room_data)

        assert response.status_code == 200
        created_room = response.json()

        assert created_room["id"] is not None

        patch_data = {
            "name": "Updated Room Name",
            "address": "Updated Address",
            "capacity": 100,
        }

        response = await test_client.patch(f"/room/{created_room['id']}", json=patch_data)

        assert response.status_code == 200
        updated_room = response.json()

        assert updated_room is not None
        assert updated_room["name"] == patch_data["name"]
        assert updated_room["address"] == patch_data["address"]
        assert updated_room["capacity"] == patch_data["capacity"]

        await RoomDao(test_session).delete_by_id(uuid.UUID(created_room["id"]))

    async def test_get_room_by_id_not_found(self, test_client):
        non_existent_id = str(uuid.uuid4())

        response = await test_client.get(f"/room/{non_existent_id}")

        assert response.status_code == 404

    async def test_delete_room_by_id_not_found(self, test_client):
        non_existent_id = str(uuid.uuid4())

        response = await test_client.delete(f"/room/{non_existent_id}")

        assert response.status_code == 404

    async def test_patch_room_by_id_not_found(self, test_client):
        non_existent_id = str(uuid.uuid4())
        patch_data = {
            "name": "Updated Room Name",
            "address": "Updated Address",
            "capacity": 100,
        }

        response = await test_client.patch(f"/room/{non_existent_id}", json=patch_data)

        assert response.status_code == 404

