from fastapi import APIRouter

from ...api.routes.v1.info import router as info_router
from ...api.routes.v1.quiz import router as quiz_router
from ...api.routes.v1.user import router as user_router

router = APIRouter(prefix="/v1")

router.include_router(
    router=info_router,
    tags=["info"],
)

router.include_router(
    router=quiz_router,
    tags=["quiz"],
)

router.include_router(
    router=user_router,
    tags=["user"],
)
