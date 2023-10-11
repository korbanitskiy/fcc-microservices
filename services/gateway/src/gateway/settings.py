from functools import cache

import pydantic


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


class MongoDBSettings(BaseSettings):
    MONGODB_HOST: str = "localhost"
    MONGODB_PORT: int = 27017


class ServicesAddressSettings(BaseSettings):
    AUTH_SERVICE_ADDRESS: str
    VIDEO_CONVERTER_SERVICE_ADDRESS: str


class AppSettings(BaseSettings):
    db = MongoDBSettings()
    services = ServicesAddressSettings()


@cache
def get_app_settings() -> AppSettings:
    return AppSettings()
