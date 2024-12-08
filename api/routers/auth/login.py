from fastapi import FastAPI, Depends, HTTPException, Request, status, Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app import app
from routers.models import LoginRequest, LoginResponse, LoginPageResponse
from auth.config import ACCESS_TOKEN_EXPIRE_MINUTES
from auth.token import verify_token
from auth.user import authenticate_user
from db.user import get_user_by_email

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
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
    except JWTError:
        raise credentials_exception
    
    email = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user
    

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
async def login(login_data: LoginRequest, response: Response):
    user, token = authenticate_user(login_data)

    # Set the token as an HTTP-only cookie
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,  # Prevent JavaScript access
        secure=True,    # Use HTTPS in production
        samesite="strict",  # CSRF protection
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Token expiration
    )

    return LoginResponse(token=token)

@app.post("/api/auth/logout")
async def logout(response: Response):
    response.delete_cookie("auth_token")
    return {"message": "Logged out successfully"}

@app.get("/api/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "You are logged in as " + current_user["email"]}
