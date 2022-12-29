from typing import Callable
from fastapi import FastAPI
from redis.asyncio import Redis
from .stubs import (
    provide_redis_stub,
    provide_session_stub,
    provide_mediator_stub,
    provide_read_quiz_service_stub,
    provide_quiz_solution_service_stub,
    provide_auth_service_stub,
    provide_user_reader_service_stub,
    provide_current_user_stub,
    provide_auth_dao_stub,
)

from .providers.auth import get_current_user
from .providers.mediator import provide_mediator
from .providers.db import provide_auth_dao
from .providers.services import (
    provide_read_quiz_service,
    provide_quiz_solution_service,
    provide_auth_service,
    provide_user_reader_service,
)


def setup(app: FastAPI, redis: Redis, session_factory: Callable):

    # Provide db
    app.dependency_overrides[provide_redis_stub] = lambda: redis
    app.dependency_overrides[provide_session_stub] = session_factory

    # Provide auth
    app.dependency_overrides[provide_current_user_stub] = get_current_user
    app.dependency_overrides[provide_auth_dao_stub] = provide_auth_dao

    # Provide mediator
    app.dependency_overrides[provide_mediator_stub] = provide_mediator

    # provide services
    app.dependency_overrides[
        provide_read_quiz_service_stub
    ] = provide_read_quiz_service

    app.dependency_overrides[
        provide_quiz_solution_service_stub
    ] = provide_quiz_solution_service

    app.dependency_overrides[
        provide_user_reader_service_stub
    ] = provide_user_reader_service

    app.dependency_overrides[provide_auth_service_stub] = provide_auth_service
