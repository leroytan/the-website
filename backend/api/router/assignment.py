import api.router.mock as mock
from api.config import settings
from api.logic.assignment_logic import AssignmentLogic
from api.logic.filter_logic import FilterLogic
from api.logic.logic import Logic
from api.logic.sort_logic import SortLogic
from api.router.auth_utils import RouterAuthUtils
from fastapi import Depends
from api.storage.models import User
from fastapi import Response
from api.router.models import (AssignmentOwnerView, AssignmentPublicView,
                               AssignmentRequestView, NewAssignment,
                               NewAssignmentRequest, SearchQuery, SearchResult, ModifiedAssignmentRequest)
from api.storage.models import Assignment, User
from fastapi import APIRouter, Depends, HTTPException, Request, Response

router = APIRouter()

@router.get("/api/assignments")
async def search_assignments(request: Request, query: str = "", filter_by: str = "", sort_by: str = "", page_size: int = 10, page_number: int = 1, debug: str = None) -> SearchResult[AssignmentPublicView]:
    if settings.is_use_mock:
        return mock.get_assignments()
    
    # Parse the filters and sorts from the query string
    # TODO: Implement a more robust parsing method
    filter_ids = filter_by.split(",") if filter_by else []

    search_query = SearchQuery(
        query=query,
        filter_by=filter_ids,
        sort_by=sort_by,
        page_size=page_size,
        page_number=page_number
    )

    try:
        user = RouterAuthUtils.get_current_user(request)
    except HTTPException:
        user = None

    res = AssignmentLogic.search_assignments(search_query, user.id if user else None)

    return SearchResult[AssignmentPublicView](
        results=res["results"],
        filters=FilterLogic.get_filters(Assignment),
        sorts=SortLogic.get_sorts(Assignment),
        num_pages=res["num_pages"],
        debug=[getattr(assignment, debug, None) for assignment in res["results"]] if debug else [],
    )


@router.post("/api/assignments/new")
async def new_assignment(new_assignment: NewAssignment, user: User = Depends(RouterAuthUtils.get_current_user)) -> AssignmentOwnerView:
    if settings.is_use_mock:
        return mock.get_assignments()[0]
    
    return AssignmentLogic.new_assignment(new_assignment, user.id)

@router.get("/api/assignments/{id}")
async def get_assignment(id: int, request: Request, response: Response) -> AssignmentOwnerView | AssignmentPublicView:
    if settings.is_use_mock:
        return mock.get_assignments()[0]
    
    try:
        user = RouterAuthUtils.get_current_user(request)
    except HTTPException:
        user = None
    
    return AssignmentLogic.get_assignment_by_id(id, user.id if user else None)

@router.put("/api/assignments/{id}")
async def update_assignment(id: int, assignment: NewAssignment, user: User = Depends(RouterAuthUtils.get_current_user)) -> AssignmentPublicView:
    if settings.is_use_mock:
        return mock.get_assignments()[0]
    
    assert_user_authorized = Logic.create_assert_user_authorized(user.id)
    
    return AssignmentLogic.update_assignment_by_id(id, assignment, assert_user_authorized)

@router.post("/api/assignment-requests/new")
async def request_assignment(assignment_request: NewAssignmentRequest, request: Request, user: User = Depends(RouterAuthUtils.get_current_user)) -> Response:
    if settings.is_use_mock:
        return Response(200)

    origin = request.headers.get("origin", "http://localhost:3000")
    AssignmentLogic.request_assignment(assignment_request, user.id, origin)
    return {"message": "Assignment requested successfully."}

@router.get("/api/assignment-requests/{id}")
async def get_assignment_request(id: int, user: User = Depends(RouterAuthUtils.get_current_user)) -> AssignmentRequestView:
    if settings.is_use_mock:
        return mock.get_assignments()[0]
    
    assert_user_authorized = Logic.create_assert_user_authorized(user.id)
    return AssignmentLogic.get_assignment_request_by_id(id, assert_user_authorized)

@router.put("/api/assignment-requests/{id}")
async def update_assignment_request(id: int, assignment_request: ModifiedAssignmentRequest, user: User = Depends(RouterAuthUtils.get_current_user)) -> AssignmentRequestView:
    if settings.is_use_mock:
        return mock.get_assignments()[0]
    
    assert_user_authorized = Logic.create_assert_user_authorized(user.id)
    return AssignmentLogic.update_assignment_request_by_id(id, assignment_request, assert_user_authorized)

@router.put("/api/assignment-requests/{id}/change-status")
async def change_assignment_request_status(id: int, status: str, user: User = Depends(RouterAuthUtils.get_current_user)) -> Response:
    if settings.is_use_mock:
        return Response(200)
    
    assert_user_authorized = Logic.create_assert_user_authorized(user.id)
    AssignmentLogic.change_assignment_request_status(id, status, assert_user_authorized)
    return {"message": "Assignment request status changed successfully."}

@router.post("/test/api/accept-assignment/{id}")
async def accept_assignment(id: int) -> Response:
    if settings.is_use_mock:
        return Response(200)

    AssignmentLogic.accept_assignment_request(id)
    return {"message": "Assignment accepted successfully."}