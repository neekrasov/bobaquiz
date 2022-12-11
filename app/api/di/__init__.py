from typing import Callable
from fastapi import FastAPI
from redis.asyncio import Redis
from .stubs import (
    provide_redis_stub,
    provide_session_stub,
    provide_redis_strategy_stub,
    provide_user_manager_stub,
)

from .providers.auth import (
    provide_redis_strategy,
    provide_user_manager,
)


def setup(app: FastAPI, redis: Redis, session_factory: Callable):

    # Provide db
    app.dependency_overrides[provide_redis_stub] = lambda: redis
    app.dependency_overrides[provide_session_stub] = session_factory

    # Provide auth
    app.dependency_overrides[
        provide_redis_strategy_stub
    ] = provide_redis_strategy
    app.dependency_overrides[provide_user_manager_stub] = provide_user_manager
