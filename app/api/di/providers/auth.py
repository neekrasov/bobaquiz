from typing import AsyncGenerator
from fastapi import Depends
from redis.asyncio import Redis
from fastapi_users.authentication import RedisStrategy

from app.services.manager import UserManager
from app.api.di.stubs import provide_redis_stub
from app.api.di.providers.db import provide_user_db


def provide_redis_strategy(
    redis: Redis = Depends(provide_redis_stub),
) -> RedisStrategy:
    return RedisStrategy(redis, lifetime_seconds=3600)


async def provide_user_manager(
    user_db=Depends(provide_user_db),
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)
