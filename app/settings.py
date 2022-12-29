from datetime import timedelta
from pydantic import BaseSettings, validator, SecretStr
from typing import Any

from app.core.user.entities.user import (
    Username,
    Email,
    HashedPassword,
)


class Settings(BaseSettings):
    project_name: str = "Project Name"
    description: str = "Project Description"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_url: str | None = None

    postgres_host: str = "localhost"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "postgres"
    postgres_url: str | None = None

    secret_key: SecretStr = SecretStr("secret")

    superuser_name: Username = Username("admin")
    superuser_email: Email = Email("admin@admin.com")
    superuser_password: HashedPassword = HashedPassword("admin")

    access_token_expire: timedelta = timedelta(minutes=30)
    refresh_token_expire: timedelta = timedelta(days=30)

    @validator("postgres_url", pre=True)
    def validate_postgres_conn(
        cls, v: str | None, values: dict[str, Any]
    ) -> str:

        if isinstance(v, str):
            return v

        return "{scheme}://{user}:{password}@{host}/{db}".format(
            scheme="postgresql+asyncpg",
            user=values.get("postgres_user"),
            password=values.get("postgres_password"),
            host=values.get("postgres_host"),
            db=values.get("postgres_db"),
        )

    @validator("redis_url", pre=True)
    def validate_redis_conn(cls, v: str | None, values: dict[str, Any]) -> str:

        if isinstance(v, str):
            return v

        return "redis://{host}:{port}".format(
            host=values.get("redis_host"),
            port=values.get("redis_port"),
        )


def get_settings():
    return Settings()
