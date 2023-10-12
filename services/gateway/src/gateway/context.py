from typing import Annotated

import pymongo
from fastapi import Depends

from gateway.app import app
from gateway import clients, services, settings


def get_app_settings() -> settings.AppSettings:
    return settings.get_app_settings()


def get_message_bus() -> clients.MessageBusClient:
    return app.state.message_bus


def get_mongodb() -> pymongo.MongoClient:
    return app.state.mongodb.client


def get_auth_client(app_settings: Annotated[settings.AppSettings, Depends(get_app_settings)]) -> clients.AuthClient:
    return clients.AuthClient(app_settings)


def get_gateway_service(
    message_bus: Annotated[clients.MessageBusClient, Depends(get_message_bus)],
    mongodb: Annotated[pymongo.MongoClient, Depends(get_mongodb)],
) -> services.GatewayService:
    return services.GatewayService(
        message_bus,
        mongodb
    )
