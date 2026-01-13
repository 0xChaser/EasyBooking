import pytest
from fastapi_users.authentication import JWTStrategy
from unittest.mock import MagicMock
import uuid

from easy_booking.auth.auth import auth_backend, bearer_transport, get_jwt_strategy
from easy_booking.settings import settings


@pytest.mark.asyncio
class TestAuthBackend:
    def test_bearer_transport_scheme_name(self):
        assert bearer_transport.scheme.scheme_name == "OAuth2PasswordBearer"

    def test_get_jwt_strategy_returns_jwt_strategy(self):
        strategy = get_jwt_strategy()
        
        assert isinstance(strategy, JWTStrategy)
        assert strategy.lifetime_seconds == settings.token_lifetime_in_seconds

    def test_auth_backend_configuration(self):
        assert auth_backend.name == "jwt"
        assert auth_backend.transport == bearer_transport
        
    async def test_jwt_strategy_write_token(self):
        strategy = get_jwt_strategy()
        
        mock_user = MagicMock()
        mock_user.id = uuid.uuid4()
        
        token = await strategy.write_token(mock_user)
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
        assert len(token.split(".")) == 3

    async def test_jwt_strategy_with_invalid_token_returns_none(self):
        strategy = get_jwt_strategy()
        invalid_token = "invalid.token.string"
        
        result = await strategy.read_token(invalid_token, user_manager=None)
        assert result is None

    def test_auth_backend_strategy_getter(self):
        strategy_getter = auth_backend.get_strategy
        strategy = strategy_getter()
        
        assert isinstance(strategy, JWTStrategy)
        assert strategy.lifetime_seconds == settings.token_lifetime_in_seconds
