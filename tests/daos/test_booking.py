from unittest.mock import patch
import uuid

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.daos.booking import BookingDao
from easy_booking.daos.room import RoomDao
from easy_booking.daos.user import UserDao
from easy_booking.exceptions.booking import BookingLinkedToAnotherObject
from tests.utils.fake_data_generator import FakeDataGenerator


@pytest.mark.asyncio
class TestBookingDao:
    async def test_booking_dao_crud(self, test_session: AsyncSession):
        user_dao = UserDao(test_session)
        room_dao = RoomDao(test_session)
        
        fake_user_data = FakeDataGenerator.fake_user()
        fake_room_data = FakeDataGenerator.fake_room()
        
        created_user = await user_dao.create(fake_user_data)
        created_room = await room_dao.create(fake_room_data)
        
        booking_dao = BookingDao(test_session)
        fake_booking_data = FakeDataGenerator.fake_booking_data(
            user_id=created_user.id,
            room_id=created_room.id
        )
        created_booking = await booking_dao.create(fake_booking_data)

        assert created_booking.id == fake_booking_data["id"]
        assert created_booking.user_id == fake_booking_data["user_id"]
        assert created_booking.room_id == fake_booking_data["room_id"]
        from datetime import timezone
        start_time_expected = fake_booking_data["start_time"]
        end_time_expected = fake_booking_data["end_time"]
        if start_time_expected.tzinfo is not None:
            start_time_expected = start_time_expected.astimezone(timezone.utc)
        else:
            start_time_expected = start_time_expected.replace(tzinfo=timezone.utc)
        if end_time_expected.tzinfo is not None:
            end_time_expected = end_time_expected.astimezone(timezone.utc)
        else:
            end_time_expected = end_time_expected.replace(tzinfo=timezone.utc)
        created_start = created_booking.start_time
        created_end = created_booking.end_time
        if created_start.tzinfo is not None:
            created_start = created_start.astimezone(timezone.utc)
        else:
            created_start = created_start.replace(tzinfo=timezone.utc)
        if created_end.tzinfo is not None:
            created_end = created_end.astimezone(timezone.utc)
        else:
            created_end = created_end.replace(tzinfo=timezone.utc)
        assert abs(created_start.timestamp() - start_time_expected.timestamp()) < 1
        assert abs(created_end.timestamp() - end_time_expected.timestamp()) < 1

        retrieved_booking = await booking_dao.get_by_id(created_booking.id)
        assert retrieved_booking.id == created_booking.id
        assert retrieved_booking.user is not None
        assert retrieved_booking.room is not None

        bookings_list = await booking_dao.get_all(offset=0, limit=10)
        assert any(booking.id == created_booking.id for booking in bookings_list)

        count = await booking_dao.count()
        assert count == 1

        deleted_booking = await booking_dao.delete_by_id(created_booking.id)
        assert deleted_booking.id == created_booking.id
        assert await booking_dao.get_by_id(created_booking.id) is None

    async def test_booking_dao_delete_with_integrity_error(self, test_session: AsyncSession):
        user_dao = UserDao(test_session)
        room_dao = RoomDao(test_session)
        
        fake_user_data = FakeDataGenerator.fake_user()
        fake_room_data = FakeDataGenerator.fake_room()
        
        created_user = await user_dao.create(fake_user_data)
        created_room = await room_dao.create(fake_room_data)
        
        booking_dao = BookingDao(test_session)
        fake_booking_data = FakeDataGenerator.fake_booking_data(
            user_id=created_user.id,
            room_id=created_room.id
        )

        created_booking = await booking_dao.create(fake_booking_data)

        assert created_booking.id == fake_booking_data["id"]

        with patch.object(test_session, "execute") as mock_execute:
            mock_execute.side_effect = IntegrityError(
                statement="DELETE FROM bookings WHERE bookings.id = :id",
                params={"id": created_booking.id},
                orig=Exception("FOREIGN KEY constraint failed"),
            )

            with pytest.raises(BookingLinkedToAnotherObject):
                await booking_dao.delete_by_id(created_booking.id)

        assert await booking_dao.get_by_id(created_booking.id) is not None

    async def test_booking_dao_delete_all(self, test_session: AsyncSession):
        user_dao = UserDao(test_session)
        room_dao = RoomDao(test_session)
        booking_dao = BookingDao(test_session)

        await booking_dao.delete_all()

        initial_count = await booking_dao.count()
        assert initial_count == 0

        fake_user_data = FakeDataGenerator.fake_user()
        fake_room_data = FakeDataGenerator.fake_room()
        
        created_user = await user_dao.create(fake_user_data)
        created_room = await room_dao.create(fake_room_data)

        created_bookings = []

        for _ in range(3):
            fake_booking_data = FakeDataGenerator.fake_booking_data(
                user_id=created_user.id,
                room_id=created_room.id
            )
            created_booking = await booking_dao.create(fake_booking_data)
            created_bookings.append(created_booking)

        count_after_creation = await booking_dao.count()
        assert count_after_creation == 3

        all_bookings = await booking_dao.get_all(offset=0, limit=10)
        assert len(all_bookings) == 3

        await booking_dao.delete_all()

        final_count = await booking_dao.count()
        assert final_count == 0

        empty_bookings = await booking_dao.get_all(offset=0, limit=10)
        assert len(empty_bookings) == 0

        for booking in created_bookings:
            retrieved_booking = await booking_dao.get_by_id(booking.id)
            assert retrieved_booking is None

