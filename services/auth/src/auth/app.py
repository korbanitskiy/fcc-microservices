from fastapi import FastAPI

from auth import views, models


def create_app():
    app = FastAPI()
    app.include_router(views.login_router)
    app.include_router(views.users_router)
    app.state.database = models.database
    return app


app = create_app()


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
