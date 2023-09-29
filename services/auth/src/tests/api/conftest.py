import pytest
from auth.app import create_app
from fastapi import FastAPI
from httpx import AsyncClient


@pytest.fixture(scope="session")
async def test_app():
    app = create_app()
    return app


@pytest.fixture(scope="session")
async def http_client(test_app: FastAPI):
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        client.cookies["X-Auth-Token"] = "auth_token"
        yield client
