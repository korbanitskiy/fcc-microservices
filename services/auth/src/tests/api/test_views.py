from unittest.mock import ANY

from tests.factories import UserFactory


async def test_health_check(http_client):
    response = await http_client.get("/health-check")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_login_unknown_user(http_client):
    form_data = {"username": "user", "password": "password"}
    response = await http_client.post("/login", data=form_data)

    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Incorrect username or password"}


async def test_login_existing_user(http_client):
    user = await UserFactory.create()
    form_data = {"username": user.name, "password": "password"}
    response = await http_client.post("/login", data=form_data)

    assert response.status_code == 200, response.text
    assert response.json() == {"access_token": ANY, "token_type": "bearer"}
