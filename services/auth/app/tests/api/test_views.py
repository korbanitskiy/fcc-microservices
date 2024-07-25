from unittest.mock import ANY

from httpx import AsyncClient

from auth import models

from ..factories import UserFactory


async def test_health_check(http_client: AsyncClient):
    response = await http_client.get("/health-check")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_login_unknown_user(http_client: AsyncClient):
    form_data = {"username": "unknown-user", "password": "password"}
    response = await http_client.post("/login", data=form_data)

    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Incorrect username or password"}


async def test_login_existing_user(http_client: AsyncClient):
    user = await UserFactory.create()
    form_data = {"username": user.name, "password": "password"}
    response = await http_client.post("/login", data=form_data)

    assert response.status_code == 200, response.text
    assert response.json() == {"access_token": ANY, "token_type": "bearer"}


async def test_access_by_token(http_client: AsyncClient):
    user = await UserFactory.create()
    form_data = {"username": user.name, "password": "password"}
    login_response = await http_client.post("/login", data=form_data)
    token = login_response.json()["access_token"]

    user_response = await http_client.get(
        "/users/me", follow_redirects=True, headers={"Authorization": f"bearer {token}"}
    )

    assert user_response.status_code == 200
    assert user_response.json() == user.dict()


async def test_get_users_list(http_client: AsyncClient, admin_user: models.User):
    users = [admin_user] + await UserFactory.create_batch(2)

    response = await http_client.get("/users")

    assert response.status_code == 200, response.text
    assert response.json() == [u.dict() for u in users]
