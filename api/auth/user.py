from fastapi import APIRouter, HTTPException, status
from db.user import get_user_by_email
from exceptions import EmailNotFoundError
from auth.password import verify_password
from auth.token import create_access_token
from routers.models import LoginRequest

def authenticate_user(login_data: LoginRequest) -> tuple:
    try:
        user = get_user_by_email(login_data.email)
    except EmailNotFoundError as e:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    token = create_access_token(data={"sub": login_data.email})
    return user, token