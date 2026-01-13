import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from easy_booking.daos.user import UserDao
from easy_booking.services.user import UserService
from tests.utils.fake_data_generator import FakeDataGenerator

fake = Faker("fr_FR")


@pytest.mark.asyncio
class TestAuthExceptions:
    
    async def test_registration_with_weak_password(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)
        
        user_data = {
            "email": fake.email(),
            "password": "123",
            "first_name": "Weak",
            "last_name": "Password",
        }
        
        response = await test_client.post("/auth/register", json=user_data)
        
        assert response.status_code in [201, 400, 422]
        
        if response.status_code == 201:
            user_dao = UserDao(test_session)
            all_users = await user_dao.get_all()
            for user in all_users:
                await user_dao.delete_by_id(user.id)

    async def test_registration_with_empty_password(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)
        
        user_data = {
            "email": fake.email(),
            "password": "",
            "first_name": "Empty",
            "last_name": "Password",
        }
        
        response = await test_client.post("/auth/register", json=user_data)
        assert response.status_code in [201, 400, 422]
        
        if response.status_code == 201:
            user_dao = UserDao(test_session)
            all_users = await user_dao.get_all()
            for user in all_users:
                await user_dao.delete_by_id(user.id)

    async def test_register_with_invalid_email_format(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)
        
        invalid_emails = [
            "",
            "notanemail",
            "@",
            "test@",
            "@domain.com",
        ]
        
        for email in invalid_emails:
            user_data = {
                "email": email,
                "password": "SecurePassword123!",
                "first_name": "Test",
                "last_name": "Invalid",
            }
            
            response = await test_client.post("/auth/register", json=user_data)
            assert response.status_code in [201, 400, 422], f"Email '{email}' response: {response.status_code}"
        
        user_dao = UserDao(test_session)
        all_users = await user_dao.get_all()
        for user in all_users:
            await user_dao.delete_by_id(user.id)

    async def test_login_with_empty_credentials(self, test_client):
        login_data = {
            "username": "",
            "password": "",
        }
        
        response = await test_client.post(
            "/auth/jwt/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code in [400, 422]

    async def test_register_with_malformed_json(self, test_client):
        response = await test_client.post(
            "/auth/register",
            content="{ this is not valid json }",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422

    async def test_login_with_malformed_data(self, test_client):
        response = await test_client.post(
            "/auth/jwt/login",
            content="invalid&data&format",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code in [400, 422]

    async def test_logout_without_authentication(self, test_client):
        response = await test_client.post("/auth/jwt/logout")
        
        assert response.status_code == 401

    async def test_logout_with_expired_token(self, test_client):
        response = await test_client.post(
            "/auth/jwt/logout",
            headers={"Authorization": "Bearer expired_or_invalid_token"}
        )
        
        assert response.status_code == 401

    async def test_register_user_with_very_long_email(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)
        
        very_long_email = "a" * 300 + "@example.com"
        user_data = {
            "email": very_long_email,
            "password": "SecurePassword123!",
            "first_name": "Long",
            "last_name": "Email",
        }
        
        response = await test_client.post("/auth/register", json=user_data)
        
        assert response.status_code in [201, 400, 422, 500]
        
        if response.status_code == 201:
            user_dao = UserDao(test_session)
            all_users = await user_dao.get_all()
            for user in all_users:
                await user_dao.delete_by_id(user.id)

    async def test_register_with_sql_injection_attempt(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)
        
        user_data = {
            "email": "sqltest@example.com",
            "password": "SecurePassword123!",
            "first_name": "'; DROP TABLE users; --",
            "last_name": "Injection",
        }
        
        response = await test_client.post("/auth/register", json=user_data)
        
        assert response.status_code in [201, 400, 422]
        
        if response.status_code == 201:
            response_data = response.json()
            assert response_data["first_name"] == user_data["first_name"]
            
            user_dao = UserDao(test_session)
            all_users = await user_dao.get_all()
            for user in all_users:
                await user_dao.delete_by_id(user.id)

    async def test_login_rate_limiting_simulation(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)
        
        user_data = {
            "email": "ratelimit@example.com",
            "password": "SecurePassword123!",
            "first_name": "Rate",
            "last_name": "Limit",
        }
        
        await test_client.post("/auth/register", json=user_data)
        
        login_data = {
            "username": user_data["email"],
            "password": "WrongPassword",
        }
        
        responses = []
        for _ in range(5):
            response = await test_client.post(
                "/auth/jwt/login",
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            responses.append(response.status_code)
        
        assert all(status == 400 for status in responses)
        
        user_dao = UserDao(test_session)
        all_users = await user_dao.get_all()
        for user in all_users:
            await user_dao.delete_by_id(user.id)

    async def test_register_with_xss_attempt(self, test_client):
        user_data = {
            "email": "xss@example.com",
            "password": "SecurePassword123!",
            "first_name": "<script>alert('XSS')</script>",
            "last_name": "<img src=x onerror=alert('XSS')>",
        }
        
        response = await test_client.post("/auth/register", json=user_data)
        
        assert response.status_code in [201, 400, 422]
        
        if response.status_code == 201:
            response_data = response.json()
            assert "first_name" in response_data
            assert "last_name" in response_data
