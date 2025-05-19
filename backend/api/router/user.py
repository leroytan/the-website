from api.logic.user_logic import UserLogic
from api.router.models import UserView
from fastapi import APIRouter

router = APIRouter()

@router.get("/api/user/{id}")
async def get_user(id: int) -> UserView:
    return UserLogic.get_user_by_id(id)