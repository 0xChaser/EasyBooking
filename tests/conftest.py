import asyncio
import sys
from pathlib import Path
from collections.abc import AsyncGenerator
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from httpx import ASGITransport, AsyncClient
from easy_booking.db import get_session
from easy_booking.main import app
from easy_booking.models.base import Base
import logging
import os
import sentry_sdk

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.WARNING)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop_policy():
    return asyncio.get_event_loop_policy()

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool,
        echo=False,
    )
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="session")
async def test_db(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="session")
async def test_session_factory(test_engine):
    return async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
        expire_on_commit=False,
    )

@pytest_asyncio.fixture(scope="session")
async def test_session(test_session_factory, test_db) -> AsyncGenerator[AsyncSession, None]:
    async with test_session_factory() as session:
        yield session
        await session.rollback()

@pytest.fixture(scope="session")
def override_get_session(test_session):
    async def _override_get_session():
        yield test_session
    return _override_get_session

@pytest_asyncio.fixture(scope="session")
async def test_client(test_app):
    async with AsyncClient(
        transport=ASGITransport(app=test_app),
        base_url="http://test"
    ) as async_client:
        yield async_client

@pytest.fixture(scope="session")
def test_app(override_get_session):
    app.dependency_overrides[get_session] = override_get_session
    yield app
    app.dependency_overrides = {}

@pytest.fixture(autouse=True, scope="session")
def disable_sentry():
    os.environ["SENTRY_DSN"] = ""
    os.environ["SENTRY_ENVIRONMENT"] = "test"
    
    try:
        sentry_sdk.init(dsn=None)
    except ImportError:
        pass