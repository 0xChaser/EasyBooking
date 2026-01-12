from enum import Enum
from functools import lru_cache

from pydantic import Field, HttpUrl, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(str, Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"
    TRACE = "trace"


class Settings(BaseSettings):

    database_uri: PostgresDsn

    secret_key: SecretStr
    token_lifetime_in_seconds: int = 3600
    algorithm: str
    date_format: str

    host: str = "127.0.0.1"
    port: int = Field(default=8000, gt=0, lt=65535)
    workers: int | None = None
    proxy_headers: bool = False
    log_level: LogLevel = LogLevel.INFO

    model_config = SettingsConfigDict(env_file=(".env", ".env.local", ".env.prod"), extra="ignore")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()