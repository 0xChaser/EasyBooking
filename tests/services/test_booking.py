import uuid
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.daos.booking import BookingDao
from easy_booking.daos.room import RoomDao
from easy_booking.daos.user import UserDao
from easy_booking.exceptions.booking import BookingNotFound
from easy_booking.schemas.page import Page
from easy_booking.services.booking import BookingService
from tests.utils.fake_data_generator import FakeDataGenerator


@pytest.mark.asyncio
class TestBookingService:
    async def test_add_booking(self, test_session: AsyncSession):
        user_dao = UserDao(test_session)
        room_dao = RoomDao(test_session)
        
        fake_user_data = FakeDataGenerator.fake_user()
        fake_room_data = FakeDataGenerator.fake_room()
        
        created_user = await user_dao.create(fake_user_data)
        created_room = await room_dao.create(fake_room_data)
        
        fake_booking_data = FakeDataGenerator.fake_booking_in(
            override={"room_id": created_room.id}
        )
        created_booking = await BookingService.add_booking(
            fake_booking_data, 
            test_session, 
            created_user.id
        )

        assert created_booking.id is not None
        assert created_booking.user_id == created_user.id
        assert created_booking.room_id == created_room.id
        assert created_booking.user is not None
        assert created_booking.room is not None

        retrieved_booking = await BookingService.get_by_id(created_booking.id, test_session)
        assert retrieved_booking is not None
        assert retrieved_booking.id == created_booking.id

        await BookingDao(test_session).delete_by_id(created_booking.id)

    async def test_get_all_booking(self, test_session: AsyncSession):
        await BookingService.delete_all(test_session)

        user_dao = UserDao(test_session)
        room_dao = RoomDao(test_session)
        
        fake_user_data = FakeDataGenerator.fake_user()
        fake_room_data = FakeDataGenerator.fake_room()
        
        created_user = await user_dao.create(fake_user_data)
        created_room = await room_dao.create(fake_room_data)

        created_bookings = []

        for i in range(3):
            fake_booking_data = FakeDataGenerator.fake_booking_in(
                override={
                    "room_id": created_room.id,
                    "start_time": datetime.now(timezone.utc) + timedelta(days=i),
                    "end_time": datetime.now(timezone.utc) + timedelta(days=i, hours=2)
                }
            )
            created_booking = await BookingService.add_booking(
                fake_booking_data, 
                test_session, 
                created_user.id
            )
            created_bookings.append(created_booking)

        page_result = await BookingService.get_all_booking(0, 10, test_session)

        assert isinstance(page_result, Page)
        assert page_result.total == 3
        assert len(page_result.items) == 3
        assert page_result.offset == 0
        assert page_result.limit == 10

        booking_ids = [booking.id for booking in page_result.items]
        for booking in created_bookings:
            assert booking.id in booking_ids

        await BookingService.delete_all(test_session)

    async def test_get_booking_by_id(self, test_session: AsyncSession):
        user_dao = UserDao(test_session)
        room_dao = RoomDao(test_session)
        
        fake_user_data = FakeDataGenerator.fake_user()
        fake_room_data = FakeDataGenerator.fake_room()
        
        created_user = await user_dao.create(fake_user_data)
        created_room = await room_dao.create(fake_room_data)
        
        fake_booking_data = FakeDataGenerator.fake_booking_in(
            override={"room_id": created_room.id}
        )
        created_booking = await BookingService.add_booking(
            fake_booking_data, 
            test_session, 
            created_user.id
        )

        retrieved_booking = await BookingService.get_by_id(created_booking.id, test_session)

        assert retrieved_booking.id == created_booking.id
        assert retrieved_booking.user_id == created_booking.user_id
        assert retrieved_booking.room_id == created_booking.room_id
        assert retrieved_booking.user is not None
        assert retrieved_booking.room is not None

        await BookingDao(test_session).delete_by_id(created_booking.id)

    async def test_get_booking_by_id_not_found(self, test_session: AsyncSession):
        non_existent_id = uuid.uuid4()

        with pytest.raises(BookingNotFound):
            await BookingService.get_by_id(non_existent_id, test_session)

    async def test_update_by_id(self, test_session: AsyncSession):
        user_dao = UserDao(test_session)
        room_dao = RoomDao(test_session)
        
        fake_user_data = FakeDataGenerator.fake_user()
        fake_room_data = FakeDataGenerator.fake_room()
        
        created_user = await user_dao.create(fake_user_data)
        created_room = await room_dao.create(fake_room_data)
        
        fake_booking_data = FakeDataGenerator.fake_booking_in(
            override={"room_id": created_room.id}
        )
        created_booking = await BookingService.add_booking(
            fake_booking_data, 
            test_session, 
            created_user.id
        )

        from easy_booking.schemas.booking import BookingPatch
        from datetime import datetime, timedelta, timezone
        
        new_start_time = datetime.now(timezone.utc) + timedelta(days=1)
        new_end_time = new_start_time + timedelta(hours=2)
        
        booking_patch = BookingPatch(
            room_id=created_room.id,
            start_time=new_start_time,
            end_time=new_end_time
        )
        
        updated_booking = await BookingService.update_by_id(
            created_booking.id, 
            booking_patch, 
            test_session
        )

        assert updated_booking.start_time == new_start_time
        assert updated_booking.end_time == new_end_time
        assert updated_booking.user is not None
        assert updated_booking.room is not None

        await BookingDao(test_session).delete_by_id(created_booking.id)

    async def test_update_by_id_not_found(self, test_session: AsyncSession):
        non_existent_id = uuid.uuid4()
        from easy_booking.schemas.booking import BookingPatch
        from datetime import datetime, timedelta, timezone
        
        start_time = datetime.now(timezone.utc)
        booking_patch = BookingPatch(
            room_id=uuid.uuid4(),
            start_time=start_time,
            end_time=start_time + timedelta(hours=2)
        )

        with pytest.raises(BookingNotFound):
            await BookingService.update_by_id(non_existent_id, booking_patch, test_session)

    async def test_delete_by_id(self, test_session: AsyncSession):
        user_dao = UserDao(test_session)
        room_dao = RoomDao(test_session)
        
        fake_user_data = FakeDataGenerator.fake_user()
        fake_room_data = FakeDataGenerator.fake_room()
        
        created_user = await user_dao.create(fake_user_data)
        created_room = await room_dao.create(fake_room_data)
        
        fake_booking_data = FakeDataGenerator.fake_booking_in(
            override={"room_id": created_room.id}
        )
        created_booking = await BookingService.add_booking(
            fake_booking_data, 
            test_session, 
            created_user.id
        )

        assert await BookingDao(test_session).get_by_id(created_booking.id) is not None

        deleted_booking = await BookingService.delete_by_id(created_booking.id, test_session)

        assert deleted_booking.id == created_booking.id

        assert await BookingDao(test_session).get_by_id(created_booking.id) is None

    async def test_delete_by_id_not_found(self, test_session: AsyncSession):
        non_existent_id = uuid.uuid4()

        with pytest.raises(BookingNotFound):
            await BookingService.delete_by_id(non_existent_id, test_session)

    async def test_delete_all(self, test_session: AsyncSession):
        booking_dao = BookingDao(test_session)
        await booking_dao.delete_all()

        user_dao = UserDao(test_session)
        room_dao = RoomDao(test_session)
        
        fake_user_data = FakeDataGenerator.fake_user()
        fake_room_data = FakeDataGenerator.fake_room()
        
        created_user = await user_dao.create(fake_user_data)
        created_room = await room_dao.create(fake_room_data)

        for i in range(3):
            fake_booking_data = FakeDataGenerator.fake_booking_in(
                override={
                    "room_id": created_room.id,
                    "start_time": datetime.now(timezone.utc) + timedelta(days=i),
                    "end_time": datetime.now(timezone.utc) + timedelta(days=i, hours=2)
                }
            )
            await BookingService.add_booking(
                fake_booking_data, 
                test_session, 
                created_user.id
            )

        count_before = await booking_dao.count()
        assert count_before == 3

        result = await BookingService.delete_all(test_session)

        assert result == []

        count_after = await booking_dao.count()
        assert count_after == 0

