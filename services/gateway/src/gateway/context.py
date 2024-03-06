from typing import Annotated

from fastapi import Depends

from gateway import clients, services, settings
from starlette.requests import Request


def get_app_settings() -> settings.AppSettings:
    return settings.get_app_settings()


def get_message_bus(request: Request) -> clients.MessageBusClient:
    return request.app.state.message_bus


def get_mongodb(request: Request) -> clients.MongoDBClient:
    return request.app.state.mongodb.client


def get_auth_client(app_settings: Annotated[settings.AppSettings, Depends(get_app_settings)]) -> clients.AuthClient:
    return clients.AuthClient(app_settings)


def get_gateway_service(
    message_bus: Annotated[clients.MessageBusClient, Depends(get_message_bus)],
    mongodb: Annotated[clients.MongoDBClient, Depends(get_mongodb)],
) -> services.GatewayService:
    return services.GatewayService(message_bus, mongodb)
