import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.daos.room import RoomDao
from easy_booking.exceptions.room import RoomNotFound
from easy_booking.schemas.page import Page
from easy_booking.services.room import RoomService
from tests.utils.fake_data_generator import FakeDataGenerator


@pytest.mark.asyncio
class TestRoomService:
    async def test_add_room(self, test_session: AsyncSession):
        fake_room_data = FakeDataGenerator.fake_room_in()
        created_room = await RoomService.add_room(fake_room_data, test_session)

        assert created_room.id is not None
        assert created_room.name == fake_room_data.name
        assert created_room.address == fake_room_data.address
        assert created_room.capacity == fake_room_data.capacity

        retrieved_room = await RoomService.get_by_id(created_room.id, test_session)
        assert retrieved_room is not None
        assert retrieved_room.id == created_room.id

        await RoomDao(test_session).delete_by_id(created_room.id)

    async def test_get_all_room(self, test_session: AsyncSession):
        await RoomService.delete_all(test_session)

        created_rooms = []

        for _ in range(3):
            fake_room_data = FakeDataGenerator.fake_room_in()
            created_room = await RoomService.add_room(fake_room_data, test_session)
            created_rooms.append(created_room)

        page_result = await RoomService.get_all_room(0, 10, test_session)

        assert isinstance(page_result, Page)
        assert page_result.total == 3
        assert len(page_result.items) == 3
        assert page_result.offset == 0
        assert page_result.limit == 10

        room_ids = [room.id for room in page_result.items]
        for room in created_rooms:
            assert room.id in room_ids

        await RoomService.delete_all(test_session)

    async def test_get_room_by_id(self, test_session: AsyncSession):
        fake_room_data = FakeDataGenerator.fake_room_in()
        created_room = await RoomService.add_room(fake_room_data, test_session)

        retrieved_room = await RoomService.get_by_id(created_room.id, test_session)

        assert retrieved_room.id == created_room.id
        assert retrieved_room.name == created_room.name
        assert retrieved_room.address == created_room.address
        assert retrieved_room.capacity == created_room.capacity

        await RoomDao(test_session).delete_by_id(created_room.id)

    async def test_get_room_by_id_not_found(self, test_session: AsyncSession):
        non_existent_id = uuid.uuid4()

        with pytest.raises(RoomNotFound):
            await RoomService.get_by_id(non_existent_id, test_session)

    async def test_update_by_id(self, test_session: AsyncSession):
        fake_room_data = FakeDataGenerator.fake_room_in()
        created_room = await RoomService.add_room(fake_room_data, test_session)

        from easy_booking.schemas.room import RoomPatch
        room_patch = RoomPatch(name="Updated Room", address="Updated Address", capacity=100)
        
        updated_room = await RoomService.update_by_id(created_room.id, room_patch, test_session)

        assert updated_room.name == "Updated Room"
        assert updated_room.address == "Updated Address"
        assert updated_room.capacity == 100

        await RoomDao(test_session).delete_by_id(created_room.id)

    async def test_update_by_id_not_found(self, test_session: AsyncSession):
        non_existent_id = uuid.uuid4()
        from easy_booking.schemas.room import RoomPatch
        room_patch = RoomPatch(
            name="Updated Room",
            address="Updated Address",
            capacity=50
        )

        with pytest.raises(RoomNotFound):
            await RoomService.update_by_id(non_existent_id, room_patch, test_session)

    async def test_delete_by_id(self, test_session: AsyncSession):
        fake_room_data = FakeDataGenerator.fake_room_in()
        created_room = await RoomService.add_room(fake_room_data, test_session)

        assert await RoomDao(test_session).get_by_id(created_room.id) is not None

        deleted_room = await RoomService.delete_by_id(created_room.id, test_session)

        assert deleted_room.id == created_room.id

        assert await RoomDao(test_session).get_by_id(created_room.id) is None

    async def test_delete_by_id_not_found(self, test_session: AsyncSession):
        non_existent_id = uuid.uuid4()

        with pytest.raises(RoomNotFound):
            await RoomService.delete_by_id(non_existent_id, test_session)

    async def test_delete_all(self, test_session: AsyncSession):
        room_dao = RoomDao(test_session)
        await room_dao.delete_all()

        for _ in range(3):
            fake_room_data = FakeDataGenerator.fake_room_in()
            await RoomService.add_room(fake_room_data, test_session)

        count_before = await room_dao.count()
        assert count_before == 3

        result = await RoomService.delete_all(test_session)

        assert result == []

        count_after = await room_dao.count()
        assert count_after == 0

