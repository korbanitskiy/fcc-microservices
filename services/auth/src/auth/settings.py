from functools import cache

import pydantic


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_USER: str

    @property
    def uri(self) -> str:
        return pydantic.PostgresDsn.build(
            scheme="postgresql",
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=str(self.DB_PORT),
            path="/" + self.DB_NAME,
        )


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
