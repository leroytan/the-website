import api.router.mock as mock
from api.config import settings
from api.logic.filter_logic import FilterLogic
from api.logic.tutor_logic import TutorLogic
from api.router.auth_utils import RouterAuthUtils
from api.router.models import (NewTutorProfile, SearchQuery, SearchResult,
                               TutorProfile, TutorPublicSummary)
from api.storage.models import Tutor, User
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel

router = APIRouter()

@router.get("/api/tutors")
async def search_tutors(query: str = "", filters: str = "", sorts: str = "", page_size: int = 10, page_number: int = 1) -> SearchResult[TutorPublicSummary]:
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
    
    # Parse the filters and sorts from the query string
    # TODO: Implement a more robust parsing method
    filter_ids = filters.split(",") if filters else []
    sort_ids = sorts.split(",") if sorts else []

    search_query = SearchQuery(
        query=query,
        filters=filter_ids,
        sorts=sort_ids,
        page_size=page_size,
        page_number=page_number
    )

    res = TutorLogic.search_tutors(search_query)
    filters = FilterLogic.get_filters(Tutor)

    return SearchResult[TutorPublicSummary](
        results=res["results"],
        filters=filters,
        num_pages=res["num_pages"],
    )


@router.post("/api/tutors/new")
async def new_tutor(
    tutorProfile: NewTutorProfile,
    user: User = Depends(RouterAuthUtils.get_current_user)
) -> TutorProfile:
    # Returns the newly created tutor profile

    if settings.is_use_mock:
        return mock.new_tutor()
    
    return TutorLogic.new_tutor(tutorProfile, user.id)

@router.get("/api/tutors/{id}")
async def get_tutor_profile(id: int, request: Request) -> TutorPublicSummary | TutorProfile | None:
    
    if settings.is_use_mock:
        return mock.get_tutor_profile()
    
    try:
        user = RouterAuthUtils.get_current_user(request)
        is_self = user and user.id == id
    except HTTPException:
        is_self = False
    return TutorLogic.find_profile_by_id(id, is_self=is_self)


@router.put("/api/tutors/{id}")
async def update_tutor_profile(
    tutorProfile: TutorProfile,
    id: int,
    user: User = Depends(RouterAuthUtils.get_current_user)
) -> TutorProfile:
    # Returns the updated private profile

    if settings.is_use_mock:
        return mock.update_tutor_profile()
    
    if user.id != id:
        raise HTTPException(status_code=403, detail="Unauthorized action")
    
    return TutorLogic.update_profile(tutorProfile, id)
