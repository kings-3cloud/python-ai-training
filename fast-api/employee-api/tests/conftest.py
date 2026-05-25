from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlmodel import create_engine, SQLModel, Session

from app.db import get_session
from app.main import fastapi_app

pytest_plugins = ("anyio",)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def test_engine():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
async def client(test_engine) -> AsyncGenerator[AsyncClient, None]:
    def override_get_session():
        with Session(test_engine) as session:
            yield session

    fastapi_app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as ac:
        yield ac
    fastapi_app.dependency_overrides.clear()
