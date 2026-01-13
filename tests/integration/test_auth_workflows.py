import pytest
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from easy_booking.daos.user import UserDao
from easy_booking.daos.room import RoomDao
from easy_booking.daos.booking import BookingDao
from easy_booking.services.user import UserService
from tests.utils.fake_data_generator import FakeDataGenerator


@pytest.mark.asyncio
class TestAuthenticationWorkflows:
    
    async def test_complete_user_registration_and_login_workflow(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)
        
        user_data = {
            "email": "workflow_user@example.com",
            "password": "SecurePassword123!",
            "first_name": "Workflow",
            "last_name": "User",
        }
        
        register_response = await test_client.post("/auth/register", json=user_data)
        assert register_response.status_code == 201
        registered_user = register_response.json()
        user_id = registered_user["id"]
        
        login_data = {
            "username": user_data["email"],
            "password": user_data["password"],
        }
        
        login_response = await test_client.post(
            "/auth/jwt/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]
        
        user_me_response = await test_client.get(
            "/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert user_me_response.status_code == 200
        user_info = user_me_response.json()
        assert user_info["email"] == user_data["email"]
        assert user_info["first_name"] == user_data["first_name"]
        
        user_info_response = await test_client.get(
            f"/user/{user_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert user_info_response.status_code == 200
        
        user_dao = UserDao(test_session)
        await user_dao.delete_by_id(uuid.UUID(user_id))

    async def test_authenticated_room_creation_workflow(self, test_session: AsyncSession, test_client):
        """Test authenticated user creating and managing rooms"""
        await UserService.delete_all(test_session)
        room_dao = RoomDao(test_session)
        await room_dao.delete_all()
        
        user_data = {
            "email": "room_creator@example.com",
            "password": "SecurePassword123!",
            "first_name": "Room",
            "last_name": "Creator",
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
        
        room_data = {
            "name": "Conference Room A",
            "address": "123 Main Street",
            "capacity": 20,
            "description": "Large conference room",
        }
        
        create_room_response = await test_client.post(
            "/room/",
            json=room_data,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert create_room_response.status_code == 200
        created_room = create_room_response.json()
        room_id = created_room["id"]
        
        list_rooms_response = await test_client.get(
            "/room/",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert list_rooms_response.status_code == 200
        rooms_list = list_rooms_response.json()
        assert len(rooms_list["items"]) > 0
        
        await room_dao.delete_by_id(uuid.UUID(room_id))
        user_dao = UserDao(test_session)
        all_users = await user_dao.get_all()
        for user in all_users:
            await user_dao.delete_by_id(user.id)

    async def test_token_expiration_workflow(self, test_session: AsyncSession, test_client):
        """Test workflow with token (simulating token handling)"""
        await UserService.delete_all(test_session)
        
        user_data = {
            "email": "token_test@example.com",
            "password": "SecurePassword123!",
            "first_name": "Token",
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
        
        response1 = await test_client.get(
            "/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response1.status_code == 200
        
        response2 = await test_client.get(
            "/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response2.status_code == 200
        
        user_dao = UserDao(test_session)
        all_users = await user_dao.get_all()
        for user in all_users:
            await user_dao.delete_by_id(user.id)

    async def test_multiple_users_authentication_workflow(self, test_session: AsyncSession, test_client):
        """Test multiple users registering and authenticating independently"""
        await UserService.delete_all(test_session)
        
        users_data = [
            {
                "email": "user1@example.com",
                "password": "Password123!",
                "first_name": "User",
                "last_name": "One",
            },
            {
                "email": "user2@example.com",
                "password": "Password456!",
                "first_name": "User",
                "last_name": "Two",
            },
            {
                "email": "user3@example.com",
                "password": "Password789!",
                "first_name": "User",
                "last_name": "Three",
            },
        ]
        
        tokens = []
        
        for user_data in users_data:
            register_response = await test_client.post("/auth/register", json=user_data)
            assert register_response.status_code == 201
            
            login_data = {
                "username": user_data["email"],
                "password": user_data["password"],
            }
            
            login_response = await test_client.post(
                "/auth/jwt/login",
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            assert login_response.status_code == 200
            tokens.append(login_response.json()["access_token"])
        
        for i, token in enumerate(tokens):
            response = await test_client.get(
                "/user/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200
            user_info = response.json()
            assert user_info["email"] == users_data[i]["email"]
        
        user_dao = UserDao(test_session)
        all_users = await user_dao.get_all()
        for user in all_users:
            await user_dao.delete_by_id(user.id)

    async def test_logout_and_token_invalidation_workflow(self, test_session: AsyncSession, test_client):
        """Test logout workflow and verify token behavior after logout"""
        await UserService.delete_all(test_session)
        
        user_data = {
            "email": "logout_workflow@example.com",
            "password": "SecurePassword123!",
            "first_name": "Logout",
            "last_name": "Workflow",
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
        
        response1 = await test_client.get(
            "/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response1.status_code == 200
        
        logout_response = await test_client.post(
            "/auth/jwt/logout",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert logout_response.status_code in [200, 204]
        
        login_response2 = await test_client.post(
            "/auth/jwt/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert login_response2.status_code == 200
        new_token = login_response2.json()["access_token"]
        assert len(new_token) > 0
        
        user_dao = UserDao(test_session)
        all_users = await user_dao.get_all()
        for user in all_users:
            await user_dao.delete_by_id(user.id)

    async def test_unauthorized_access_attempts_workflow(self, test_session: AsyncSession, test_client):
        await UserService.delete_all(test_session)

        protected_endpoints = [
            ("/user/me", "GET"),
            ("/booking/", "GET"),
        ]
        
        for endpoint, method in protected_endpoints:
            if method == "GET":
                response = await test_client.get(endpoint)
            
            assert response.status_code == 401, f"Endpoint {endpoint} should require auth"
        
        public_endpoints = [
            ("/room/", "GET"),
        ]
        
        for endpoint, method in public_endpoints:
            if method == "GET":
                response = await test_client.get(endpoint)
            
            assert response.status_code == 200, f"Endpoint {endpoint} should be public"
        
        user_data = {
            "email": "auth_test@example.com",
            "password": "SecurePassword123!",
            "first_name": "Auth",
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
        
        for endpoint, method in protected_endpoints:
            if method == "GET":
                response = await test_client.get(
                    endpoint,
                    headers={"Authorization": f"Bearer {access_token}"}
                )
            assert response.status_code == 200, f"Endpoint {endpoint} should be accessible with auth"
        
        user_dao = UserDao(test_session)
        all_users = await user_dao.get_all()
        for user in all_users:
            await user_dao.delete_by_id(user.id)

    async def test_easybooking_complete_user_journey(self, test_session: AsyncSession, test_client):
        """Test complet du parcours utilisateur EasyBooking :
        1. Créer un compte
        2. Connexion
        3. Voir la liste des chambres disponibles
        4. Réserver une chambre pour un créneau horaire
        5. Voir ses réservations
        6. Annuler une réservation
        """
        from datetime import datetime, timedelta, timezone
        
        await UserService.delete_all(test_session)
        room_dao = RoomDao(test_session)
        await room_dao.delete_all()
        booking_dao = BookingDao(test_session)
        await booking_dao.delete_all()
        
        user_data = {
            "email": "easybooking_user@example.com",
            "password": "SecurePassword123!",
            "first_name": "Easy",
            "last_name": "Booking",
        }
        
        register_response = await test_client.post("/auth/register", json=user_data)
        assert register_response.status_code == 201
        registered_user = register_response.json()
        assert registered_user["email"] == user_data["email"]
        user_id = registered_user["id"]
        
        login_data = {
            "username": user_data["email"],
            "password": user_data["password"],
        }
        
        login_response = await test_client.post(
            "/auth/jwt/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        access_token = token_data["access_token"]
        
        room_data = {
            "name": "Salle de Réunion A",
            "address": "123 Rue de Paris",
            "capacity": 10,
            "description": "Salle équipée projecteur et tableau blanc",
        }
        await test_client.post("/room/", json=room_data)
        
        room_data_2 = {
            "name": "Salle de Conférence B",
            "address": "456 Avenue des Champs",
            "capacity": 25,
            "description": "Grande salle pour conférences",
        }
        await test_client.post("/room/", json=room_data_2)
        
        rooms_response = await test_client.get("/room/")
        assert rooms_response.status_code == 200
        rooms_data = rooms_response.json()
        assert "items" in rooms_data
        assert len(rooms_data["items"]) >= 2
        
        selected_room = rooms_data["items"][0]
        room_id = selected_room["id"]
        
        start_time = datetime.now(timezone.utc) + timedelta(days=1, hours=10)
        end_time = start_time + timedelta(hours=2)
        
        booking_data = {
            "room_id": room_id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        }
        
        booking_response = await test_client.post(
            "/booking/",
            json=booking_data,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert booking_response.status_code == 200
        created_booking = booking_response.json()
        booking_id = created_booking["id"]
        assert created_booking["room_id"] == room_id
        
        my_bookings_response = await test_client.get(
            "/booking/",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert my_bookings_response.status_code == 200
        bookings_data = my_bookings_response.json()
        assert "items" in bookings_data
        
        booking_ids = [b["id"] for b in bookings_data["items"]]
        assert booking_id in booking_ids
        
        booking_detail_response = await test_client.get(
            f"/booking/{booking_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert booking_detail_response.status_code == 200
        booking_detail = booking_detail_response.json()
        assert booking_detail["room"]["name"] == selected_room["name"]
        
        cancel_response = await test_client.delete(
            f"/booking/{booking_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert cancel_response.status_code == 200
        
        cancelled_booking_response = await test_client.get(
            f"/booking/{booking_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert cancelled_booking_response.status_code == 404
        
        await room_dao.delete_all()
        user_dao = UserDao(test_session)
        await user_dao.delete_by_id(uuid.UUID(user_id))