from unittest.mock import patch

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.daos.room import RoomDao
from easy_booking.exceptions.room import RoomLinkedToAnotherObject
from tests.utils.fake_data_generator import FakeDataGenerator


@pytest.mark.asyncio
class TestRoomDao:
    async def test_room_dao_crud(self, test_session: AsyncSession):
        room_dao = RoomDao(test_session)
        await room_dao.delete_all()
        
        fake_room_data = FakeDataGenerator.fake_room()
        created_room = await room_dao.create(fake_room_data)

        assert created_room.id == fake_room_data["id"]
        assert created_room.name == fake_room_data["name"]
        assert created_room.address == fake_room_data["address"]
        assert created_room.capacity == fake_room_data["capacity"]

        retrieved_room = await room_dao.get_by_id(created_room.id)
        assert retrieved_room.id == created_room.id

        rooms_list = await room_dao.get_all(offset=0, limit=10)
        assert any(room.id == created_room.id for room in rooms_list)

        count = await room_dao.count()
        assert count == 1

        deleted_room = await room_dao.delete_by_id(created_room.id)
        assert deleted_room.id == created_room.id
        assert await room_dao.get_by_id(created_room.id) is None

    async def test_room_dao_delete_with_integrity_error(self, test_session: AsyncSession):
        room_dao = RoomDao(test_session)
        fake_room_data = FakeDataGenerator.fake_room()

        created_room = await room_dao.create(fake_room_data)

        assert created_room.id == fake_room_data["id"]

        with patch.object(test_session, "execute") as mock_execute:
            mock_execute.side_effect = IntegrityError(
                statement="DELETE FROM rooms WHERE rooms.id = :id",
                params={"id": created_room.id},
                orig=Exception("FOREIGN KEY constraint failed"),
            )

            with pytest.raises(RoomLinkedToAnotherObject):
                await room_dao.delete_by_id(created_room.id)

        assert await room_dao.get_by_id(created_room.id) is not None

    async def test_room_dao_delete_all(self, test_session: AsyncSession):
        room_dao = RoomDao(test_session)

        await room_dao.delete_all()

        initial_count = await room_dao.count()
        assert initial_count == 0

        created_rooms = []

        for _ in range(3):
            fake_room_data = FakeDataGenerator.fake_room()
            created_room = await room_dao.create(fake_room_data)
            created_rooms.append(created_room)

        count_after_creation = await room_dao.count()
        assert count_after_creation == 3

        all_rooms = await room_dao.get_all(offset=0, limit=10)
        assert len(all_rooms) == 3

        await room_dao.delete_all()

        final_count = await room_dao.count()
        assert final_count == 0

        empty_rooms = await room_dao.get_all(offset=0, limit=10)
        assert len(empty_rooms) == 0

        for room in created_rooms:
            retrieved_room = await room_dao.get_by_id(room.id)
            assert retrieved_room is None

