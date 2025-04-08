import api.router.mock as mock
from api.config import settings
from api.router.models import Assignment
from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

router = APIRouter()

@router.get("/api/assignments")
async def get_assignments() -> list[Assignment]:
    if settings.is_use_mock:
        return mock.get_assignments()
    
    raise NotImplementedError("Assignment retrieval is not yet implemented.")

@router.post("/api/assignments/create")
async def create_assignment(request: Request, response: Response) -> Assignment:
    if settings.is_use_mock:
        return mock.get_assignments()[0]
    
    raise NotImplementedError("Assignment creation is not yet implemented.")

@router.get("/api/assignments/item/{assignment_id}")
async def get_assignment(assignment_id: int) -> Assignment:
    if settings.is_use_mock:
        return mock.get_assignments()[0]
    
    raise NotImplementedError("Assignment retrieval is not yet implemented.")

@router.put("/api/assignments/item/{assignment_id}")
async def update_assignment(assignment: Assignment, assignment_id: int) -> Assignment:
    if settings.is_use_mock:
        return mock.get_assignments()[0]
    
    raise NotImplementedError("Assignment update is not yet implemented.")

class IncomingAssignmentRequest(BaseModel):
    tutor_id: int
    datetime: str

@router.post("/api/assignments/request/{assignment_id}")
async def request_assignment(details: IncomingAssignmentRequest, assignment_id: int) -> Assignment:
    if settings.is_use_mock:
        return Response(200)
    
    raise NotImplementedError("Assignment request is not yet implemented.")