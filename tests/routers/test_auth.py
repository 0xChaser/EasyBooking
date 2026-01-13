import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from easy_booking.daos.user import UserDao
from easy_booking.services.user import UserService
from tests.utils.fake_data_generator import FakeDataGenerator

fake = Faker("fr_FR")


@pytest.mark.asyncio
class TestAuthRouter:
    
    async def test_register_user(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)
        
        user_data = {
            "email": fake.email(),
            "password": "SecurePassword123!",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        }
        
        response = await test_client.post("/auth/register", json=user_data)
        
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["email"] == user_data["email"]
        assert response_data["first_name"] == user_data["first_name"]
        assert response_data["last_name"] == user_data["last_name"]
        assert "id" in response_data
        assert "hashed_password" not in response_data
        assert "password" not in response_data
        
        user_dao = UserDao(test_session)
        all_users = await user_dao.get_all()
        for user in all_users:
            await user_dao.delete_by_id(user.id)

    async def test_register_user_duplicate_email(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)
        
        user_data = {
            "email": "duplicate@example.com",
            "password": "SecurePassword123!",
            "first_name": "John",
            "last_name": "Doe",
        }
        
        response1 = await test_client.post("/auth/register", json=user_data)
        assert response1.status_code == 201
        
        response2 = await test_client.post("/auth/register", json=user_data)
        assert response2.status_code == 400
        
        user_dao = UserDao(test_session)
        all_users = await user_dao.get_all()
        for user in all_users:
            await user_dao.delete_by_id(user.id)

    async def test_register_user_invalid_email(self, test_client):
        user_data = {
            "email": "@",
            "password": "SecurePassword123!",
            "first_name": "John",
            "last_name": "Doe",
        }
        
        response = await test_client.post("/auth/register", json=user_data)
        assert response.status_code in [201, 400, 422]

    async def test_register_user_email_must_be_valid_format(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)
        
        invalid_emails = [
            "plaintext",
            "missing@domain",
            "@nodomain.com",
            "spaces in@email.com",
            "double@@at.com",
        ]
        
        for invalid_email in invalid_emails:
            user_data = {
                "email": invalid_email,
                "password": "SecurePassword123!",
                "first_name": "Test",
                "last_name": "User",
            }
            
            response = await test_client.post("/auth/register", json=user_data)
            assert response.status_code in [201, 400, 422], f"Email '{invalid_email}' should be validated"
        
        user_dao = UserDao(test_session)
        all_users = await user_dao.get_all()
        for user in all_users:
            await user_dao.delete_by_id(user.id)

    async def test_register_user_valid_email_accepted(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)
        
        valid_emails = [
            "simple@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user123@example.org",
        ]
        
        for valid_email in valid_emails:
            user_data = {
                "email": valid_email,
                "password": "SecurePassword123!",
                "first_name": "Test",
                "last_name": "User",
            }
            
            response = await test_client.post("/auth/register", json=user_data)
            assert response.status_code == 201, f"Valid email '{valid_email}' should be accepted"
        
        user_dao = UserDao(test_session)
        all_users = await user_dao.get_all()
        for user in all_users:
            await user_dao.delete_by_id(user.id)

    async def test_register_user_missing_required_fields(self, test_client):
        """Test registration with missing required fields"""
        user_data = {
            "email": "test@example.com",
        }
        
        response = await test_client.post("/auth/register", json=user_data)
        assert response.status_code == 422

    async def test_login_with_valid_credentials(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)
        
        user_data = {
            "email": "login_test@example.com",
            "password": "SecurePassword123!",
            "first_name": "Login",
            "last_name": "Test",
        }
        
        register_response = await test_client.post("/auth/register", json=user_data)
        assert register_response.status_code == 201
        
        login_data = {
            "username": user_data["email"],
            "password": user_data["password"],
        }
        
        response = await test_client.post(
            "/auth/jwt/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"
        assert len(response_data["access_token"]) > 0
        
        user_dao = UserDao(test_session)
        all_users = await user_dao.get_all()
        for user in all_users:
            await user_dao.delete_by_id(user.id)

    async def test_login_with_invalid_password(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)
        
        user_data = {
            "email": "invalid_login@example.com",
            "password": "SecurePassword123!",
            "first_name": "Invalid",
            "last_name": "Login",
        }
        
        register_response = await test_client.post("/auth/register", json=user_data)
        assert register_response.status_code == 201
        
        login_data = {
            "username": user_data["email"],
            "password": "WrongPassword123!",
        }
        
        response = await test_client.post(
            "/auth/jwt/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 400
        
        user_dao = UserDao(test_session)
        all_users = await user_dao.get_all()
        for user in all_users:
            await user_dao.delete_by_id(user.id)

    async def test_login_with_nonexistent_user(self, test_client):
        """Test login with non-existent user"""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "SomePassword123!",
        }
        
        response = await test_client.post(
            "/auth/jwt/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 400

    async def test_logout(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)
        
        user_data = {
            "email": "logout_test@example.com",
            "password": "SecurePassword123!",
            "first_name": "Logout",
            "last_name": "Test",
        }
        
        await test_client.post("/auth/register", json=user_data)
        
        login_data = {
            "username": user_data["email"],
            "password": user_data["password"],
        }
        
        login_response = await test_client.post(
            "/auth/jwt/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        access_token = login_response.json()["access_token"]
        
        response = await test_client.post(
            "/auth/jwt/logout",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        assert response.status_code == 200 or response.status_code == 204
        
        user_dao = UserDao(test_session)
        all_users = await user_dao.get_all()
        for user in all_users:
            await user_dao.delete_by_id(user.id)

    async def test_protected_endpoint_without_token(self, test_client):
        response = await test_client.get("/user/")
        
        assert response.status_code == 401

    async def test_protected_endpoint_with_invalid_token(self, test_client):
        response = await test_client.get(
            "/user/",
            headers={"Authorization": "Bearer invalid_token_here"}
        )
        
        assert response.status_code == 401

    async def test_protected_endpoint_with_valid_token(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)
        
        user_data = {
            "email": "protected_test@example.com",
            "password": "SecurePassword123!",
            "first_name": "Protected",
            "last_name": "Test",
        }
        
        await test_client.post("/auth/register", json=user_data)
        
        login_data = {
            "username": user_data["email"],
            "password": user_data["password"],
        }
        
        login_response = await test_client.post(
            "/auth/jwt/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        access_token = login_response.json()["access_token"]
        
        response = await test_client.get(
            "/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        assert response.status_code == 200
        user_info = response.json()
        assert user_info["email"] == user_data["email"]
        
        user_dao = UserDao(test_session)
        all_users = await user_dao.get_all()
        for user in all_users:
            await user_dao.delete_by_id(user.id)
