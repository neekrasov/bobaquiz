from fastapi import FastAPI
from .stubs import (
    provide_redis_stub,
    provide_session_stub,
    provide_redis_strategy_stub,
    provide_user_manager_stub,
)

from .providers.db import (
    provide_redis,
    provide_session,
)

from .providers.auth import (
    provide_redis_strategy,
    provide_user_manager,
)


def setup_di(app: FastAPI):

    # Provide db
    app.dependency_overrides[provide_redis_stub] = lambda: provide_redis()
    app.dependency_overrides[provide_session_stub] = provide_session()

    # Provide auth
    app.dependency_overrides[
        provide_redis_strategy_stub
    ] = provide_redis_strategy
    app.dependency_overrides[provide_user_manager_stub] = provide_user_manager
