import api.router.mock as mock
from api.config import settings
from api.logic.client_logic import ClientLogic
from api.router.models import ClientProfile
from fastapi import APIRouter, Request, Response

router = APIRouter()

@router.post("/api/clients/create")
async def create_client(clientProfile: ClientProfile) -> ClientProfile:
    if settings.is_use_mock:
        return mock.create_client()
    
    raise NotImplementedError("Client creation is not yet implemented.")
    
@router.get("/api/clients/profile/{id}")
async def get_client_profile(id: str = None) -> ClientProfile | None:
    if settings.is_use_mock:
        return mock.get_client_profile()
    
    raise NotImplementedError("Client profile retrieval is not yet implemented.")

@router.put("/api/clients/profile/{id}")
async def update_client_profile(clientProfile: ClientProfile, id: str = None) -> ClientProfile | None:
    if settings.is_use_mock:
        return mock.update_client_profile()
    
    raise NotImplementedError("Client profile update is not yet implemented.")