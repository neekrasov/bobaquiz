from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.core.settings import get_settings, Settings
from src.core.di.setup import setup_di
from src.routes.router import router as api_router
from src.routes.v1.auth import setup_auth


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        description=settings.description,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
    )

    setup_di(app)
    setup_auth(app, api_router)

    app.include_router(
        router=api_router,
        prefix="/api",
    )

    return app


app = create_app(get_settings())
