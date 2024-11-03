from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from app import app
from routers.models import LoginRequest, LoginResponse, LoginPageResponse
from auth.token import create_access_token, verify_token
from auth.password import verify_password

# Dummy user database (replace with real DB in production)
users_db = {
    "user@example.com": {
        "password": "$2b$12$wsyxh9HogoHWD6Sp1EmhSeKeBwC5zrsdxHFo87ZwGSPxzuwtwlZY6",  # hashed password for "password123"
        "userType": "tutor"
    }
}

# OAuth2 scheme for bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload

@app.get("/api/auth/login", response_model=LoginPageResponse)
async def login_page(request: Request):
    return LoginPageResponse(
        title="Login to THE (Teach Learn Excel)",
        description="Please enter your email and password to log in.",
        fields=[
            {"name": "email", "type": "email", "label": "Email Address", "required": True, "placeholder": "Enter your email"},
            {"name": "password", "type": "password", "label": "Password", "required": True, "placeholder": "Enter your password"}
        ]
    )

@app.post("/api/auth/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    user = users_db.get(login_data.email)
    if not user or not verify_password(login_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    token = create_access_token(data={"sub": login_data.email, "userType": user["userType"]})
    return LoginResponse(token=token, userType=user["userType"])

@app.get("/api/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user['sub']}!"}
