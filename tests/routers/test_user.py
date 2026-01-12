import uuid

import pytest

from easy_booking.daos.user import UserDao
from easy_booking.services.user import UserService
from tests.utils.fake_data_generator import FakeDataGenerator


@pytest.mark.asyncio
class TestUserRouter:

    async def test_get_user_by_id(self, test_session, test_client):
        user_dao = UserDao(test_session)
        fake_user_data = FakeDataGenerator.fake_user()
        
        created_user = await user_dao.create(fake_user_data)

        response = await test_client.get(f"/user/{created_user.id}")

        assert response.status_code == 200
        retrieved_user = response.json()

        assert retrieved_user is not None
        assert retrieved_user["id"] == str(created_user.id)
        assert retrieved_user["email"] == created_user.email
        assert retrieved_user["first_name"] == created_user.first_name
        assert retrieved_user["last_name"] == created_user.last_name

        await user_dao.delete_by_id(created_user.id)

    async def test_get_user_by_id_not_found(self, test_client):
        non_existent_id = str(uuid.uuid4())

        response = await test_client.get(f"/user/{non_existent_id}")

        assert response.status_code == 404

    async def test_patch_user_by_id(self, test_session, test_client):
        user_dao = UserDao(test_session)
        fake_user_data = FakeDataGenerator.fake_user()
        
        created_user = await user_dao.create(fake_user_data)

        patch_data = {
            "email": "updated.email@example.com",
            "first_name": "UpdatedFirstName",
            "last_name": "UpdatedLastName",
            "password": "newpassword123",
        }

        response = await test_client.patch(f"/user/{created_user.id}", json=patch_data)

        assert response.status_code == 200
        updated_user = response.json()

        assert updated_user is not None
        assert updated_user["email"] == patch_data["email"]
        assert updated_user["first_name"] == patch_data["first_name"]
        assert updated_user["last_name"] == patch_data["last_name"]

        await user_dao.delete_by_id(created_user.id)

    async def test_patch_user_by_id_not_found(self, test_client):
        non_existent_id = str(uuid.uuid4())
        patch_data = {
            "email": "updated.email@example.com",
            "first_name": "UpdatedFirstName",
            "last_name": "UpdatedLastName",
            "password": "newpassword123",
        }

        response = await test_client.patch(f"/user/{non_existent_id}", json=patch_data)

        assert response.status_code == 404

