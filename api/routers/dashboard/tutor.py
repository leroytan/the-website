from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app import app
from routers.auth.login import get_current_user
from routers.models import User

# Dummy user database (replace with real DB in production)
users_db = {
    "user@example.com": {
        # hashed password for "password123"
        "password": "$2b$12$wsyxh9HogoHWD6Sp1EmhSeKeBwC5zrsdxHFo87ZwGSPxzuwtwlZY6",
        "userType": "tutor"
    }
}

# OAuth2 scheme for bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


@app.get("/api/dashboard/tutor")
async def dashboard_tutor(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user.email}!"}
