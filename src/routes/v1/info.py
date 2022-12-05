from fastapi import APIRouter

router = APIRouter(prefix="/info")


@router.get("/")
async def info():
    return {"message": "Hello World"}
