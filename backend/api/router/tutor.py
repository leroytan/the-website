from api.logic.tutor_logic import TutorLogic
from api.router.models import (TutorProfile, TutorPublicSummary,
                               TutorSearchQuery)
from fastapi import APIRouter, Request, Response

router = APIRouter()

@router.get("/api/tutors")
async def search_tutors(query: str = None, subjects: list = [], levels: list = []) -> list[TutorPublicSummary]:
    """
    Handles the searching of specific tutors using fields such as subjects and levels.

    Returns:
        list[TutorPublicSummary]: A list of tutor public summaries that match the search query.

    Raises: (TBC)
        HTTPException: If the login credentials are invalid or the login process 
                        fails, an HTTP error is raised with an appropriate status code.
    """

    search_query = TutorSearchQuery(
        query=query,
        subjects=subjects,
        levels=levels,
    )

    results = TutorLogic.search_tutors(search_query)

    return results

@router.get("/api/tutors/profile/{id}")
async def get_tutor_profile(id: str = None) -> TutorPublicSummary | TutorProfile | None:
    # TODO: find a way to use login authorization to differentiate between public and private profiles
    return TutorLogic.find_tutor_by_id(id)

@router.post("/api/tutors/profile/{id}")
async def update_tutor_profile(id: str = None) -> TutorProfile:
    # TODO: Enforce login authorization to access private profiles
    # Returns the updated private profile
    return TutorLogic.find_tutor_by_id(id)

@router.post("/api/tutors/request")
async def request_tutor(request: Request) -> Response:
    # TODO: Enforce login authentication for clients

    data = await request.json()
    TutorLogic.request_tutor(data)

    return Response(status_code=200)


