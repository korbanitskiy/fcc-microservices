from functools import cache

import pika
import pydantic


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


class MongoDBSettings(BaseSettings):
    MONGODB_HOST: str
    MONGODB_PORT: int


class MessageBusSettings(BaseSettings):
    MESSAGE_BUS_HOST: str
    MESSAGE_BUS_PORT: int

    @property
    def connection_params(self) -> pika.ConnectionParameters:
        return pika.ConnectionParameters(
            host=self.MESSAGE_BUS_HOST,
            port=self.MESSAGE_BUS_PORT,
        )


class ServicesAddressSettings(BaseSettings):
    AUTH_SERVICE_ADDRESS: str
    VIDEO_CONVERTER_SERVICE_ADDRESS: str


class AppSettings(BaseSettings):
    db = MongoDBSettings()
    message_bus = MessageBusSettings()
    services = ServicesAddressSettings()


@cache
def get_app_settings() -> AppSettings:
    return AppSettings()
