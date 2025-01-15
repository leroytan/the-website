from fastapi import APIRouter, Request, Response

from api.router.models import ModuleReviews

router = APIRouter()

@router.get("/api/module-reviews")
async def get_module_reviews():
    return []

@router.get("/api/module-reviews/:module-code")
async def get_module_reviews(request: Request):
    return []
