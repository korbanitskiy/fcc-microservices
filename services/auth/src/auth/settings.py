from functools import cache

import pydantic
import pydantic_settings


class BaseSettings(pydantic_settings.BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


class DBSettings(BaseSettings):
    DB_URI: pydantic.PostgresDsn
    DB_POOL_SIZE_MIN: int
    DB_POOL_SIZE_MAX: int
    DB_TEST: str | None = None

    @property
    def uri(self) -> str:
        if self.DB_TEST:
            return self.DB_TEST

        return str(self.DB_URI)


class AuthSettings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM = "HS256"


class AppSettings(BaseSettings):
    db = DBSettings()
    auth = AuthSettings()


@cache
def get_app_settings() -> AppSettings:
    return AppSettings()
