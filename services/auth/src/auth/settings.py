from functools import cache

import pydantic


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_POOL_SIZE_MIN: int
    DB_POOL_SIZE_MAX: int
    DB_TEST: str | None = None

    @property
    def uri(self) -> str:
        if self.DB_TEST:
            return self.DB_TEST

        return pydantic.PostgresDsn.build(
            scheme="postgresql",
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=str(self.DB_PORT),
            path="/" + self.DB_NAME,
        )


class AppSettings(BaseSettings):
    db = DBSettings()


@cache
def get_app_settings() -> AppSettings:
    return AppSettings()
