from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.infrastructure.db.factory import create_async_session, create_redis
from app.settings import get_settings, Settings
from app.api import di
from app.api.routes.router import router as api_router
from app.api.routes.v1.auth import setup_auth


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        description=settings.description,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
    )

    session_factory = create_async_session(settings.postgres_url)
    redis = create_redis(settings.redis_url)

    di.setup(
        app=app,
        redis=redis,
        session_factory=session_factory
    )

    setup_auth(
        app=app,
        router=api_router
    )

    app.include_router(
        router=api_router,
        prefix="/api",
    )

    return app


app = create_app(get_settings())
