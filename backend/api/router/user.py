from fastapi import APIRouter, HTTPException, Request, Response

from api.logic.tutor_logic import TutorLogic
from api.logic.user_logic import UserLogic
from api.router.auth_utils import RouterAuthUtils

# Removed redundant import

router = APIRouter()


@router.get("/api/user/{id}")
async def get_user(id: int, request: Request, response: Response) -> dict:
    is_self = False

    try:
        user = RouterAuthUtils.get_current_user(request)
        is_self = user.id == id
    except HTTPException as e:
        if e.status_code != 401:
            raise e

    try:
        tutor = TutorLogic.find_profile_by_id(id, is_self=is_self)
    except HTTPException as e:
        if e.status_code != 404:
            raise e
        tutor = None
    return {
        "user": UserLogic.get_user_by_id(id),
        "tutor": tutor,
    }
