from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import pymongo
from gateway import services, settings, clients, app


def get_app_settings() -> settings.AppSettings:
    return settings.get_app_settings()


def get_message_bus() -> clients.MessageBusClient:
    return app.state.message_bus


def get_mongodb() -> pymongo.MongoClient:
    return app.state.mongodb.client


def get_auth_client(settings: Annotated[settings.AppSettings, Depends(get_app_settings)]) -> clients.AuthClient:
    return clients.AuthClient(settings)


def get_gateway_service(
    auth_client: Annotated[clients.AuthClient, Depends(get_auth_client)],
) -> services.GatewayService:
    return services.GatewayService(
        auth_client,
    )