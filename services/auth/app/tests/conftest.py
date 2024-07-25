import asyncio

import pytest
import sqlalchemy

from app import models, services, settings

from .factories import UserFactory

app_settings = settings.get_app_settings()
engine = sqlalchemy.create_engine(str(models.database.url))


@pytest.fixture(scope="session", autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def create_test_database():
    models.metadata.create_all(engine)
    yield
    models.metadata.drop_all(engine)


@pytest.fixture(scope="session")
async def app_db(create_test_database):
    with models.database.force_rollback():
        async with models.database:
            yield models.database


@pytest.fixture(scope="session")
async def admin_user(app_db):
    return await UserFactory.create(name="admin")


@pytest.fixture(autouse=True)
async def db_transaction(app_db):
    print(11)
    async with app_db.transaction(force_rollback=True):
        print(12)

        yield app_db


@pytest.fixture(scope="session")
def user_service():
    return services.UserService(app_settings)
