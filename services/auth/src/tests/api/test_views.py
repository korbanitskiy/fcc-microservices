from tests.factories import UserFactory
from unittest.mock import ANY


async def test_health_check(http_client):
    response = await http_client.get("/health-check")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_login_unknown_user(http_client):
    form_data = {"username": "user", "password": "password"}
    response = await http_client.post("/login", json=form_data)

    assert response.status_code == 401
    assert response.text == "Incorrect username or password"


async def test_login_existing_user(http_client):
    user = await UserFactory.create()
    form_data = {"username": user.name, "password": user.password}
    response = await http_client.post("/login", json=form_data)

    assert response.status_code == 200
    assert response.json() == {"access_token": ANY, "token_type": "bearer"}
