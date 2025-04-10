import api.router.mock as mock
from api.config import settings
from api.logic.assignment_logic import AssignmentLogic
from api.logic.filter_logic import FilterLogic
from api.router.auth_utils import RouterAuthUtils
from api.router.models import Assignment as AssignmentView
from api.router.models import NewAssignment, SearchQuery, SearchResult
from api.storage.models import Assignment, AssignmentRequest, User
from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel

router = APIRouter()

@router.get("/api/assignments")
async def search_assignments(query: str = "", filters: str = "", sorts: str = "") -> SearchResult[AssignmentView]:
    if settings.is_use_mock:
        return mock.get_assignments()
    
    # Parse the filters and sorts from the query string
    # TODO: Implement a more robust parsing method
    filter_ids = filters.split(",") if filters else []
    sort_ids = sorts.split(",") if sorts else []

    search_query = SearchQuery(
        query=query,
        filters=filter_ids,
        sorts=sort_ids,
    )

    results = AssignmentLogic.search_assignments(search_query)
    filters = FilterLogic.get_filters(Assignment)

    return SearchResult[AssignmentView](
        results=results,
        filters=filters,
    )


@router.post("/api/assignments/create")
async def create_assignment(new_assignment: NewAssignment, user: User = Depends(RouterAuthUtils.get_current_user)) -> AssignmentView:
    if settings.is_use_mock:
        return mock.get_assignments()[0]
    
    return AssignmentLogic.create_assignment(new_assignment, user.id)

@router.get("/api/assignments/item/{assignment_id}")
async def get_assignment(assignment_id: int) -> AssignmentView:
    if settings.is_use_mock:
        return mock.get_assignments()[0]
    
    return AssignmentLogic.get_assignment_by_id(assignment_id)

@router.put("/api/assignments/item/{assignment_id}")
async def update_assignment(assignment_id: int, assignment: NewAssignment) -> AssignmentView:
    if settings.is_use_mock:
        return mock.get_assignments()[0]
    
    return AssignmentLogic.update_assignment_by_id(assignment_id, assignment)

@router.post("/api/assignments/request/{assignment_id}")
async def request_assignment(assignment_id: int, user: User = Depends(RouterAuthUtils.get_current_user)) -> Response:
    if settings.is_use_mock:
        return Response(200)
    
    AssignmentLogic.request_assignment(assignment_id, user.id)
    return {"message": "Assignment requested successfully."}