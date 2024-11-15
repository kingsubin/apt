from typing import Any

from pydantic import MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.constants import Environment


class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class Config(CustomBaseSettings):
    ENVIRONMENT: Environment = Environment.PRODUCTION

    DATABASE_URL: MySQLDsn
    DATABASE_ASYNC_URL: MySQLDsn
    DATABASE_POOL_SIZE: int = 16
    DATABASE_POOL_TTL: int = 60 * 20  # 20 minutes
    DATABASE_POOL_PRE_PING: bool = True

    CORS_ORIGINS: list[str] = ["*"]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["*"]

    APP_VERSION: str = "0.1"


settings = Config()

app_configs: dict[str, Any] = {"title": "App API"}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
