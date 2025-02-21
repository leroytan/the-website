import api.router.mock as mock
from api.config import settings
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

    if settings.is_use_mock:
        return mock.search_tutors()

    search_query = TutorSearchQuery(
        query=query,
        subjects=subjects,
        levels=levels,
    )

    results = TutorLogic.search_tutors(search_query)

    return results


@router.post("/api/tutors/create")
async def create_tutor(request: Request) -> TutorProfile:
    # TODO: Enforce login authentication for tutors
    # Returns the newly created tutor profile

    if settings.is_use_mock:
        return mock.create_tutor()

    data = await request.json()
    pass

@router.get("/api/tutors/profile/{id}")
async def get_tutor_profile(id: str = None) -> TutorPublicSummary | TutorProfile | None:
    # TODO: find a way to use login authorization to differentiate between public and private profiles
    
    if settings.is_use_mock:
        return mock.get_tutor_profile()
    pass
    # return TutorLogic.find_tutor_by_id(id)


@router.put("/api/tutors/profile/{id}")
async def update_tutor_profile(id: str = None) -> TutorProfile:
    # TODO: Enforce login authorization to access private profiles
    # Returns the updated private profile

    if settings.is_use_mock:
        return mock.update_tutor_profile()
    pass
    # return TutorLogic.find_tutor_by_id(id)


@router.post("/api/tutors/request{id}")
async def request_tutor(request: Request, id: str = None) -> Response:
    # TODO: Enforce login authentication for clients

    if settings.is_use_mock:
        return Response(status_code=200)
    pass
    # data = await request.json()
    # TutorLogic.request_tutor(data)

    # return Response(status_code=200)
