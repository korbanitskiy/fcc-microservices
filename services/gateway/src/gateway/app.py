from fastapi import FastAPI

from gateway import views, clients, settings
from tenacity import retry, stop_after_attempt, wait_fixed


settings = settings.get_app_settings()


@retry(wait=wait_fixed(5), stop=stop_after_attempt(5))
def connect_to_message_bus(message_bus: clients.MessageBusClient):
    if not message_bus.is_connected:
        message_bus.connect()


@retry(wait=wait_fixed(5), stop=stop_after_attempt(5))
def connect_to_mongodb(mongo_client: clients.MongoDBClient):
    if not mongo_client.is_connected:
        mongo_client.connect()


def create_app():
    app = FastAPI()
    app.include_router(views.router)
    app.state.message_bus = clients.MessageBusClient(settings)
    app.state.mongodb = clients.MongoDBClient(settings)
    return app


app = create_app()


@app.on_event("startup")
async def startup() -> None:
    connect_to_message_bus(app.state.message_bus)


@app.on_event("shutdown")
async def shutdown() -> None:
    message_bus: clients.MessageBusClient = app.state.message_bus
    mongodb: clients.MongoDBClient = app.state.mongodb

    if message_bus.is_connected:
        message_bus.disconnect()
    
    if mongodb.is_connected:
        mongodb.disconnect()
