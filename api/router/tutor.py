from fastapi import APIRouter

from api.auth.config import (ACCESS_TOKEN_EXPIRE_MINUTES,
                             REFRESH_TOKEN_EXPIRE_MINUTES)
from api.logic.tutor_logic import TutorLogic

router = APIRouter()

@router.get("/api/tutors")
async def get_tutors():
    tutors = TutorLogic.get_public_summaries()
    return tutors

@router.get("/api/tutor/idk")
async def tutor_idk():
    return {"message": "Hello from FastAPI tutor with everything"}