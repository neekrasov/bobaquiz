from functools import cache
from pydantic import BaseSettings, validator
from typing import Any


class Settings(BaseSettings):
    project_name: str = "Project Name"
    description: str = "Project Description"

    redis_host: str = "localhost"
    redis_port: int = 6379

    postgres_host: str = "localhost"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "postgres"
    postgres_url: str | None = None

    secret_key: str = "secret"

    superuser_name: str = "admin"
    superuser_email: str = "admin@admin.com"
    superuser_password: str = "admin"

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

    class Config:
        env_file = ".env"


@cache
def get_settings(**kwargs):
    return Settings(**kwargs)
