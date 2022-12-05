from fastapi import FastAPI, APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, AuthenticationBackend

from src.core.di.stubs import (
    provide_current_user_stub,
    provide_redis_strategy_stub,
    provide_user_manager_stub,
)

from src.schemas.users import UserCreate, UserRead, UserUpdate


def setup_auth_routes(
    router: APIRouter,
    auth_app: FastAPIUsers,
    auth_backend: AuthenticationBackend,
):
    router.include_router(
        router=auth_app.get_auth_router(auth_backend),
        prefix="/users",
        tags=["auth"],
    )

    router.include_router(
        router=auth_app.get_register_router(UserRead, UserCreate),
        prefix="/users",
        tags=["auth"],
    )
    router.include_router(
        router=auth_app.get_reset_password_router(),
        prefix="/users",
        tags=["auth"],
    )
    router.include_router(
        router=auth_app.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["users"],
    )
    return router


def setup_auth(app: FastAPI, router: APIRouter):
    auth_backend = AuthenticationBackend(
        name="redis",
        transport=BearerTransport(tokenUrl="v1/users/login"),
        get_strategy=provide_redis_strategy_stub,
    )

    auth_app = FastAPIUsers(
        get_user_manager=provide_user_manager_stub,
        auth_backends=[auth_backend],
    )

    current_user = auth_app.current_user()

    app.dependency_overrides[provide_current_user_stub] = current_user

    setup_auth_routes(router, auth_app, auth_backend)
