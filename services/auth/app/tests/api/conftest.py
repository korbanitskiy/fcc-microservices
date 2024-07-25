import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from auth import models, services
from auth.app import create_app


@pytest.fixture(scope="session")
async def test_app():
    app = create_app()
    return app


@pytest.fixture(scope="session")
async def http_client(test_app: FastAPI, admin_user: models.User, user_service: services.UserService):
    token = user_service.create_access_token(admin_user)
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        client.headers["Authorization"] = f"{token.token_type} {token.access_token}"
        yield client
