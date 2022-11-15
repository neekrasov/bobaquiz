from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.core.settings import get_settings, Settings
from src.api.router import router as api_router
from src.db.stubs import get_session_stub
from src.db.session import async_session

def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        description=settings.description,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
    )
    
    app.include_router(
        router=api_router,
        prefix="/api",
    )
    
    app.dependency_overrides[get_session_stub] = async_session(settings.postgres_uri)
    
    return app


app = create_app(get_settings())