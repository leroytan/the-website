import api.router.mock as mock
from api.config import settings
from api.logic.assignment_logic import AssignmentLogic
from api.logic.filter_logic import FilterLogic
from api.logic.logic import Logic
from api.router.auth_utils import RouterAuthUtils
from api.router.models import (AssignmentOwnerView, AssignmentPublicView,
                               NewAssignment, SearchQuery, SearchResult)
from api.storage.models import Assignment, User
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel

router = APIRouter()

@router.get("/api/assignments")
async def search_assignments(request: Request, query: str = "", filters: str = "", sorts: str = "") -> SearchResult[AssignmentPublicView]:
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

    user = None
    try:
        user = RouterAuthUtils.get_current_user(request)
    except HTTPException as e:
        if e.status_code != 401:
            raise e

    results = AssignmentLogic.search_assignments(search_query, user.id if user else None)
    filters = FilterLogic.get_filters(Assignment)

    return SearchResult[AssignmentPublicView](
        results=results,
        filters=filters,
    )


@router.post("/api/assignments/new")
async def new_assignment(new_assignment: NewAssignment, user: User = Depends(RouterAuthUtils.get_current_user)) -> AssignmentOwnerView:
    if settings.is_use_mock:
        return mock.get_assignments()[0]
    
    return AssignmentLogic.new_assignment(new_assignment, user.id)

@router.get("/api/assignments/{id}")
async def get_assignment(id: int, request: Request) -> AssignmentOwnerView | AssignmentPublicView:
    if settings.is_use_mock:
        return mock.get_assignments()[0]
    
    user = None
    try:
        user = RouterAuthUtils.get_current_user(request)
    except HTTPException as e:
        if e.status_code != 401:
            raise e
    
    return AssignmentLogic.get_assignment_by_id(id, user.id if user else None)

@router.put("/api/assignments/{id}")
async def update_assignment(id: int, assignment: NewAssignment, user: User = Depends(RouterAuthUtils.get_current_user)) -> AssignmentPublicView:
    if settings.is_use_mock:
        return mock.get_assignments()[0]
    
    assert_user_authorized = Logic.create_assert_user_authorized(user.id)
    
    return AssignmentLogic.update_assignment_by_id(id, assignment, assert_user_authorized)

@router.post("/api/assignments/{id}/request")
async def request_assignment(id: int, user: User = Depends(RouterAuthUtils.get_current_user)) -> Response:
    if settings.is_use_mock:
        return Response(200)
    
    AssignmentLogic.request_assignment(id, user.id)
    return {"message": "Assignment requested successfully."}

@router.put("/api/assignment-requests/{id}/change-status")
async def change_assignment_request_status(id: int, status: str, user: User = Depends(RouterAuthUtils.get_current_user)) -> Response:
    if settings.is_use_mock:
        return Response(200)
    
    assert_user_authorized = Logic.create_assert_user_authorized(user.id)
    AssignmentLogic.change_assignment_request_status(id, status, assert_user_authorized)
    return {"message": "Assignment request status changed successfully."}
