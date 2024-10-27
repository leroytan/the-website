from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from app import app
from routers.models import SignupRequest, SignupResponse
from auth.token import create_access_token, verify_token
from auth.password import hash_password
from db.user import create_user
from exceptions import EmailAlreadyUsedError

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
    try:
        new_user = create_user(
            email=signup_data.email,
            name=signup_data.name,
            password_hash=hashed_password,
            user_type=signup_data.userType
        )
    except EmailAlreadyUsedError as e:
        raise HTTPException(status_code=409, detail=str(e))

    # Return the created user's details (without the password)
    return SignupResponse(
        id=str(new_user.id),
        email=signup_data.email,
        name=signup_data.name,
        userType=signup_data.userType,
        token=create_access_token(data={"sub": signup_data.email, "userType": signup_data.userType})
    )
