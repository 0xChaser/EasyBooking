import pytest
from src.easy_booking.settings import get_settings, LogLevel

def test_production_security_config():
    settings = get_settings()
    assert settings.log_level not in [LogLevel.DEBUG, LogLevel.TRACE]
    assert len(settings.secret_key.get_secret_value()) >= 32

def test_no_hardcoded_secrets_in_settings():
    settings = get_settings()
    weak_keys = ["changeme", "secret", "password", "123456", "admin"]
    assert settings.secret_key.get_secret_value().lower() not in weak_keys

def test_token_lifetime_security():
    settings = get_settings()
    assert settings.token_lifetime_in_seconds <= 86400
    assert settings.token_lifetime_in_seconds >= 300

def test_hashing_algorithm_security():
    settings = get_settings()
    assert settings.algorithm in ["HS256", "RS256", "ES256"]

def test_database_connection_security():
    settings = get_settings()
    dsn = str(settings.database_uri)
    assert "postgresql" in dsn
    assert "asyncpg" in dsn

def test_server_port_security():
    settings = get_settings()
    assert settings.port > 1024
    assert settings.port != 8080

def test_workers_configuration():
    settings = get_settings()
    if settings.workers is not None:
        assert settings.workers >= 1

def test_host_binding_security():
    settings = get_settings()
    assert settings.host in ["127.0.0.1", "0.0.0.0", "localhost"]

def test_proxy_headers_security():
    settings = get_settings()
    if settings.proxy_headers:
        assert isinstance(settings.proxy_headers, bool)

def test_settings_input_validation_mode():
    settings = get_settings()
    assert settings.model_config.get("extra") == "ignore"

