from fastapi import APIRouter

from api.logic.tutor_logic import TutorLogic

from api.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.get("/api/tutors")
async def get_tutors():
    tutors = TutorLogic.get_public_summaries()
    return tutors