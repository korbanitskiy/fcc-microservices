import os

import databases
import ormar
import sqlalchemy
from auth.settings import get_app_settings
from auth.views import router
from fastapi import FastAPI

settings = get_app_settings()

metadata = sqlalchemy.MetaData()
database = databases.Database(settings.db.uri)


def create_app():
    app = FastAPI()
    app.include_router(router)
    app.state.database = database
    return app


app = create_app()


# Model should be cachable for DebugToolbar tracking
if os.getenv("DEBUG"):
    ormar.Model.__hash__ = lambda self: id(self)
