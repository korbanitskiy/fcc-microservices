from auth.services import authenticate_user
from tests.factories import UserFactory


async def test_authenticate_user_not_found():
    user = await authenticate_user("user-name", "password")

    assert user is None


async def test_authenticate_user_found():
    db_user = await UserFactory.create()
    auth_user = await authenticate_user(db_user.name, "password")

    assert auth_user == db_user
