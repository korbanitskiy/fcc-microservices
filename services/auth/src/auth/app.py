import os

from fastapi import FastAPI

from auth.views import router
from auth.models import database


def create_app():
    app = FastAPI()
    app.include_router(router)
    app.state.database = database
    return app


app = create_app()
