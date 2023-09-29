import asyncio

import pytest
import sqlalchemy
from auth.app import database, metadata

DATABASE_URL = "sqlite://"


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def create_test_database():
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture(scope="session")
async def app_db(create_test_database):
    with database.force_rollback():
        async with database:
            yield database


@pytest.fixture(autouse=True)
async def db_transaction(app_db):
    async with app_db.transaction(force_rollback=True):
        yield app_db
