from calendar import timegm
from datetime import datetime, timedelta

from freezegun import freeze_time
from tests.factories import UserFactory

from auth import services


async def test_authenticate_user_not_found(user_service: services.UserService):
    user = await user_service.authenticate_user("user-name", "password")

    assert user is None


async def test_authenticate_user_found(user_service: services.UserService):
    db_user = await UserFactory.create()
    auth_user = await user_service.authenticate_user(db_user.name, "password")

    assert auth_user == db_user


@freeze_time("2023-01-10")
async def test_encode_decode_access_token(user_service: services.UserService):
    user = await UserFactory.create()
    token = user_service.create_access_token(user, expires_minutes=10)
    payload = user_service.decode_access_token(token.access_token)
    expire_datetime = datetime.utcnow() + timedelta(minutes=10)

    assert token.access_token is not None
    assert token.token_type == "bearer"
    assert payload == {"sub": user.name, "exp": timegm(expire_datetime.utctimetuple())}
