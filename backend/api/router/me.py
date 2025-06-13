from api.logic.assignment_logic import AssignmentLogic
from api.logic.tutor_logic import TutorLogic
from api.logic.user_logic import UserLogic
from api.router.auth_utils import RouterAuthUtils
from api.router.models import (AssignmentOwnerView, AssignmentPublicView,
                                UserView, UserUpdateRequest)
from api.storage.models import User
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

router = APIRouter()

@router.post("/api/me/upload-profile-photo/")
async def upload_profile_photo(file: UploadFile = File(...), user: User = Depends(RouterAuthUtils.get_current_user)):
    if file.content_type not in ["image/jpeg", "image/png", "image/webp", "image/jpg", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid image type")
    
    file_data = await file.read()
    UserLogic.upload_profile_photo(file_data, user.id, file.content_type)
    return {
        "message": "Profile photo uploaded successfully",
        "url": UserLogic.get_profile_photo_url(user.id)
    }   

@router.get("/api/me/created-assignments")
async def get_created_assignments(user: User = Depends(RouterAuthUtils.get_current_user)) -> list[AssignmentOwnerView]:
    return AssignmentLogic.get_created_assignments(user.id)

@router.get("/api/me/applied-assignments")
async def get_applied_assignments(user: User = Depends(RouterAuthUtils.get_current_user)) -> list[AssignmentPublicView]:
    return AssignmentLogic.get_applied_assignments(user.id)

@router.get("/api/me")
async def get_user_info(user: User = Depends(RouterAuthUtils.get_current_user)) -> dict:
    try:
        tutor = TutorLogic.find_profile_by_id(user.id, is_self=True)
    except HTTPException as e:
        if e.status_code != 404:
            raise e
        tutor = None
    return {
        "user": UserLogic.get_user_by_id(user.id),
        "tutor": tutor,
    }

@router.put("/api/me")
async def update_user_info(user_update_request: UserUpdateRequest, user: User = Depends(RouterAuthUtils.get_current_user)) -> UserView:
    return UserLogic.update_user_details(user.id, user_update_request.name, user_update_request.intends_to_be_tutor)