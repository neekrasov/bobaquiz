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
    postgres_uri: str | None = None

    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7
    secret_key: str = "secret"
    
    @validator("postgres_uri", pre=True)
    def validate_postgres_conn(cls, v: str | None, values: dict[str, Any]) -> str:
        
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