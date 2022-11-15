from fastapi import APIRouter
from src.api.v1.info import router as info_router

router = APIRouter(prefix="/v1")

router.include_router(
    router=info_router,
    tags=["info"],    
)