from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from app import app
from routers.models import SignupRequest, SignupResponse
from auth.token import create_access_token, verify_token
from auth.password import hash_password

# Dummy user database (replace with real DB in production)
users_db = {
    
}

# OAuth2 scheme for bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload

@app.post("/api/auth/signup", response_model=SignupResponse)
async def signup(signup_data: SignupRequest):
    # Check if the email is already registered
    if signup_data.email in users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash the password before storing it
    hashed_password = hash_password(signup_data.password)

    # Create a new user entry with a unique ID
    user_id = str(1)
    users_db[signup_data.email] = {
        "id": user_id,
        "email": signup_data.email,
        "name": signup_data.name,
        "password": hashed_password,
        "userType": signup_data.userType,
    }

    # Return the created user's details (without the password)
    return SignupResponse(
        id=user_id,
        email=signup_data.email,
        name=signup_data.name,
        userType=signup_data.userType,
        token=create_access_token(data={"sub": signup_data.email, "userType": signup_data.userType})
    )
