import httpx
import orjson
import pika
from pymongo import MongoClient

from gateway import schemas, settings


class AuthClient:
    def __init__(self, settings: settings.AppSettings) -> None:
        self.settings = settings

    def login(self, name: str, password: str) -> schemas.Token:
        response = httpx.post(
            url=self.settings.services.AUTH_SERVICE_ADDRESS + "/login",
            data={"username": name, "password": password},
        )
        response.raise_for_status()
        return schemas.Token(**response.json())

    def get_user(self, token: str) -> schemas.User:
        response = httpx.get(
            url=self.settings.services.AUTH_SERVICE_ADDRESS + "/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        return schemas.User(**response.json())


class MessageBusClient:
    def __init__(self, app_settings: settings.AppSettings) -> None:
        self.app_settings = app_settings
        self.connection = None
        self.channel = None

    @property
    def is_connected(self):
        return self.connection is not None

    def connect(self):
        self.connection = pika.BlockingConnection(self.app_settings.message_bus.connection_params)
        self.channel = self.connection.channel()

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.channel = None

    def publish(self, queue: str, message: dict):
        if not self.is_connected:
            raise Exception("Client is not connected")

        self.channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=orjson.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent,
            ),
        )


class MongoDBClient:
    def __init__(self, settings: settings.AppSettings) -> None:
        self.settings = settings
        self.client: MongoClient  = None

    @property
    def is_connected(self) -> bool:
        return self.client is not None

    def connect(self):
        self.client = MongoClient(
            host=self.settings.db.MONGODB_HOST,
            port=self.settings.db.MONGODB_PORT,
            connect=True,
        )

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None
