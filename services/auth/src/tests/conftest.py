import asyncio

import pytest
import sqlalchemy
from auth import models, settings, services
from tests.factories import UserFactory

app_settings = settings.get_app_settings()
engine = sqlalchemy.create_engine(app_settings.db.uri, connect_args={"check_same_thread": False})


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def create_test_database():
    models.metadata.create_all(engine)
    yield
    models.metadata.drop_all(engine)


@pytest.fixture(scope="session")
async def app_db(create_test_database):
    with models.database.force_rollback():
        async with models.database:
            yield models.database


@pytest.fixture(scope="session")
async def auth_user(app_db):
    return await UserFactory.create()


@pytest.fixture(autouse=True)
async def db_transaction(app_db):
    async with app_db.transaction(force_rollback=True):
        yield app_db


@pytest.fixture(scope="session")
def user_service():
    return services.UserService(app_settings)