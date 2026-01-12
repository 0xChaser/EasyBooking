from unittest.mock import patch

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.daos.user import UserDao
from easy_booking.exceptions.user import UserLinkedToAnotherObject
from tests.utils.fake_data_generator import FakeDataGenerator
from easy_booking.schemas.user import UserCreate
from easy_booking.exceptions.base import INVALIDDATATYPE

@pytest.mark.asyncio
class TestUserDao:
    async def test_user_dao_crud(self, test_session: AsyncSession):
        user_dao = UserDao(test_session)
        await user_dao.delete_all()
        
        fake_user_data = FakeDataGenerator.fake_user()
        created_user = await user_dao.create(fake_user_data)

        assert created_user.id == fake_user_data["id"]
        assert created_user.email == fake_user_data["email"]
        assert created_user.first_name == fake_user_data["first_name"]
        assert created_user.last_name == fake_user_data["last_name"]

        retrieved_user = await user_dao.get_by_id(created_user.id)
        assert retrieved_user.id == created_user.id

        users_list = await user_dao.get_all(offset=0, limit=10)
        assert any(user.id == created_user.id for user in users_list)

        count = await user_dao.count()
        assert count == 1

        deleted_user = await user_dao.delete_by_id(created_user.id)
        assert deleted_user.id == created_user.id
        assert await user_dao.get_by_id(created_user.id) is None

    async def test_user_dao_delete_with_integrity_error(self, test_session: AsyncSession):
        user_dao = UserDao(test_session)
        fake_user_data = FakeDataGenerator.fake_user()

        created_user = await user_dao.create(fake_user_data)

        assert created_user.id == fake_user_data["id"]

        with patch.object(test_session, "execute") as mock_execute:
            mock_execute.side_effect = IntegrityError(
                statement="DELETE FROM user WHERE user.id = :id",
                params={"id": created_user.id},
                orig=Exception("FOREIGN KEY constraint failed"),
            )

            with pytest.raises(UserLinkedToAnotherObject):
                await user_dao.delete_by_id(created_user.id)

        assert await user_dao.get_by_id(created_user.id) is not None

    async def test_user_dao_delete_all(self, test_session: AsyncSession):
        user_dao = UserDao(test_session)

        await user_dao.delete_all()

        initial_count = await user_dao.count()
        assert initial_count == 0

        created_users = []

        for _ in range(3):
            fake_user_data = FakeDataGenerator.fake_user()
            created_user = await user_dao.create(fake_user_data)
            created_users.append(created_user)

        count_after_creation = await user_dao.count()
        assert count_after_creation == 3

        all_users = await user_dao.get_all(offset=0, limit=10)
        assert len(all_users) == 3

        await user_dao.delete_all()

        final_count = await user_dao.count()
        assert final_count == 0

        empty_users = await user_dao.get_all(offset=0, limit=10)
        assert len(empty_users) == 0

        for user in created_users:
            retrieved_user = await user_dao.get_by_id(user.id)
            assert retrieved_user is None