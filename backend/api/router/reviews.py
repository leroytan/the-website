from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/api/module-reviews")
async def get_module_reviews() -> list:
    return []


@router.get("/api/module-reviews/:module-code")
async def get_module_reviews(request: Request) -> list:
    return []
