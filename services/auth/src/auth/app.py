from fastapi import FastAPI

from auth import models, views
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(wait=wait_fixed(5), stop=stop_after_attempt(5))
async def connect_to_db(db):
    if not db.is_connected:
        await db.connect()


def create_app():
    app = FastAPI()
    app.include_router(views.login_router)
    app.include_router(views.users_router)
    app.state.database = models.database
    return app


app = create_app()


@app.on_event("startup")
async def startup() -> None:
    await connect_to_db(app.state.database)


@app.on_event("shutdown")
async def shutdown() -> None:
    db = app.state.database
    if db.is_connected:
        await db.disconnect()
