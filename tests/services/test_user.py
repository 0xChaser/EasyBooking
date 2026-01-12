import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.daos.user import UserDao
from easy_booking.exceptions.user import UserNotFound
from easy_booking.schemas.page import Page
from easy_booking.services.user import UserService
from tests.utils.fake_data_generator import FakeDataGenerator


@pytest.mark.asyncio
class TestUserService:
    async def test_add_user(self, test_session: AsyncSession):
        fake_user_data = FakeDataGenerator.fake_user()
        user_dao = UserDao(test_session)
        created_user = await user_dao.create(fake_user_data)

        assert created_user.id is not None
        assert created_user.email == fake_user_data["email"]
        assert created_user.first_name == fake_user_data["first_name"]
        assert created_user.last_name == fake_user_data["last_name"]

        retrieved_user = await UserService.get_user_by_id(created_user.id, test_session)
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id

        await UserDao(test_session).delete_by_id(created_user.id)

    async def test_get_all_user(self, test_session: AsyncSession):
        user_dao = UserDao(test_session)
        await UserService.delete_all(test_session)

        created_users = []

        for _ in range(3):
            fake_user_data = FakeDataGenerator.fake_user()
            created_user = await user_dao.create(fake_user_data)
            created_users.append(created_user)

        page_result = await UserService.get_all(0, 10, test_session)

        assert isinstance(page_result, Page)
        assert page_result.total == 3
        assert len(page_result.items) == 3
        assert page_result.offset == 0
        assert page_result.limit == 10

        user_ids = [user.id for user in page_result.items]
        for user in created_users:
            assert user.id in user_ids

        await UserService.delete_all(test_session)

    async def test_get_user_by_id(self, test_session: AsyncSession):
        fake_user_data = FakeDataGenerator.fake_user()
        user_dao = UserDao(test_session)
        created_user = await user_dao.create(fake_user_data)

        retrieved_user = await UserService.get_user_by_id(created_user.id, test_session)

        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email
        assert retrieved_user.first_name == created_user.first_name
        assert retrieved_user.last_name == created_user.last_name

        await user_dao.delete_by_id(created_user.id)

    async def test_get_user_by_id_not_found(self, test_session: AsyncSession):
        non_existent_id = uuid.uuid4()

        with pytest.raises(UserNotFound):
            await UserService.get_user_by_id(non_existent_id, test_session)

    async def test_update_by_id(self, test_session: AsyncSession):
        fake_user_data = FakeDataGenerator.fake_user()
        user_dao = UserDao(test_session)
        created_user = await user_dao.create(fake_user_data)

        user = await user_dao.get_by_id(created_user.id)
        user.first_name = "Updated Name"
        user.last_name = "Updated Last Name"
        user.email = "updated.email@example.com"
        await test_session.commit()

        retrieved_user = await UserService.get_user_by_id(created_user.id, test_session)
        assert retrieved_user.first_name == "Updated Name"
        assert retrieved_user.last_name == "Updated Last Name"
        assert retrieved_user.email == "updated.email@example.com"

        await user_dao.delete_by_id(created_user.id)

    async def test_update_by_id_not_found(self, test_session: AsyncSession):
        non_existent_id = uuid.uuid4()

        with pytest.raises(UserNotFound):
            await UserService.get_user_by_id(non_existent_id, test_session)

    async def test_delete_by_id(self, test_session: AsyncSession):
        fake_user_data = FakeDataGenerator.fake_user()
        user_dao = UserDao(test_session)
        created_user = await user_dao.create(fake_user_data)

        assert await user_dao.get_by_id(created_user.id) is not None

        deleted_user = await UserService.delete_by_id(created_user.id, test_session)

        assert deleted_user.id == created_user.id

        assert await user_dao.get_by_id(created_user.id) is None

    async def test_delete_by_id_not_found(self, test_session: AsyncSession):
        non_existent_id = uuid.uuid4()

        with pytest.raises(UserNotFound):
            await UserService.delete_by_id(non_existent_id, test_session)

    async def test_delete_all(self, test_session: AsyncSession):
        user_dao = UserDao(test_session)
        await user_dao.delete_all()

        for _ in range(3):
            fake_user_data = FakeDataGenerator.fake_user()
            await user_dao.create(fake_user_data)

        count_before = await user_dao.count()
        assert count_before == 3

        result = await UserService.delete_all(test_session)

        assert result == []

        count_after = await user_dao.count()
        assert count_after == 0

    async def test_get_all(self, test_session: AsyncSession):
        user_dao = UserDao(test_session)
        await UserService.delete_all(test_session)

        users_to_create = 3
        created_users = []

        for _ in range(users_to_create):
            fake_user_data = FakeDataGenerator.fake_user()
            created_user = await user_dao.create(fake_user_data)
            created_users.append(created_user)

        page_result = await UserService.get_all(0, 10, test_session)

        assert isinstance(page_result, Page)
        assert page_result.total == users_to_create
        assert len(page_result.items) == users_to_create
        assert page_result.offset == 0
        assert page_result.limit == 10

        user_ids = [user.id for user in page_result.items]
        for user in created_users:
            assert user.id in user_ids

        await UserService.delete_all(test_session)