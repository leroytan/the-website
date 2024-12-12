from fastapi import Depends, Request, Response, APIRouter

from typing import Dict

from api.router.models import LoginRequest
from api.router.models import SignupRequest

from api.logic.tutor_logic import TutorLogic

from api.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.get("/api/tutors")
async def get_tutors():
    tutors = TutorLogic.get_all_tutors()
    return tutors