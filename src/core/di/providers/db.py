from typing import AsyncGenerator
from redis.asyncio import Redis
from fastapi import Depends
from src.db.session import async_session
from src.core.settings import get_settings
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase
from src.db.models.user import User
from src.core.di.stubs import provide_session_stub


def provide_redis() -> Redis:
    redis = Redis.from_url("redis://localhost:6379", decode_responses=True)
    return redis


def provide_session():
    context_session = async_session(get_settings().postgres_uri)
    return context_session


async def provide_user_db(
    session: AsyncSession = Depends(provide_session_stub),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    yield SQLAlchemyUserDatabase(session, User)
