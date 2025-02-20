from api.logic.client_logic import ClientLogic
from api.router.models import ClientProfile
from fastapi import APIRouter, Request, Response

router = APIRouter()

@router.get("/api/clients/profile/{id}")
async def client_profile(id: str = None) -> ClientProfile | None:
    # TODO: Enforce login authorization to only allow the client to access their own profile
    return ClientLogic.find_client_by_id(id)

@router.post("/api/clients/profile/{id}")
async def client_profile(request: Request) -> ClientProfile:
    # TODO: Enforce login authorization to only allow the client to access their own profile
    # Returns the updated client profile
    data = await request.json()

    return ClientLogic.update_client_profile(data)



