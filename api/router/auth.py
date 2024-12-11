from fastapi import Depends, Request, Response, APIRouter

from typing import Dict

from api.router.models import LoginRequest
from api.router.models import SignupRequest

from api.logic.logic import Logic

from api.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES

from api.common.utils import Utils

from api.storage.models import User

router = APIRouter()

def update_tokens(tokens: Dict[str, str], response: Response) -> None:
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,  # Prevent JavaScript access
        secure=True,    # Use HTTPS in production
        samesite="strict",  # CSRF protection
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Token expiration
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,  # Prevent JavaScript access
        secure=True,    # Use HTTPS in production
        samesite="strict",  # CSRF protection
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,  # Token expiration
    )

def clear_tokens(response: Response) -> None:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

async def get_current_user(request: Request) -> User:
    token = request.cookies.get("access_token")
    print(token)
    user = Logic.get_current_user(token)
    return user

@router.post("/api/auth/login")
async def login(request: Request, response: Response):
    """
    Handles user login by validating the provided credentials and generating 
    an authentication token. The token is then set as an HTTP-only cookie in 
    the response for secure and persistent access.

    Args:
        request (Request): The request object containing the login data
        response (Response): The response object used to set the authentication 
                              token as a secure HTTP-only cookie.

    Returns:
        str: A success message confirming the login process.

    Response Cookies:
        - auth_token (str): A secure, HTTP-only authentication token set as a 
                            cookie for user session management.

    Raises:
        HTTPException: If the login credentials are invalid or the login process 
                        fails, an HTTP error is raised with an appropriate status code.
    """
    data = await request.json()

    login_data = LoginRequest(
        email=data["email"],
        password=data["password"],
        userType=Utils.str_to_user_type(data["userType"])
    )

    tokens = Logic.handle_login(login_data=login_data)
    update_tokens(tokens, response)

    response.status_code = 200

    return {"message": "Logged in successfully"}

@router.post("/api/auth/signup")
async def signup(request: Request, response: Response):
    """
    Handles user registration by processing the provided signup data, 
    creating a new user account, and generating an authentication token. 
    The token is then set as an HTTP-only cookie in the response for secure 
    and persistent access.

    Args:
        request (Request): The request object containing the signup data
        response (Response): The response object used to set the authentication 
                              token as a secure HTTP-only cookie.

    Returns:
        str: A success message confirming the signup process.

    Response Cookies:
        - auth_token (str): A secure, HTTP-only authentication token set as a 
                            cookie to manage the user's session after registration.

    Raises:
        HTTPException: If the signup process fails (e.g., due to validation errors 
                        or a conflict with existing accounts), an HTTP error is 
                        raised with an appropriate status code.
    """
    data = await request.json()

    signup_data = SignupRequest(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        userType=Utils.str_to_user_type(data["userType"])
    )
    
    tokens = Logic.handle_signup(signup_data=signup_data)
    update_tokens(tokens, response)

    response.status_code = 201

    return {"message": "Signed up successfully"}
    

@router.post("/api/auth/logout")
async def logout(response: Response):
    clear_tokens(response)
    return {"message": "Logged out successfully"}

@router.get("/api/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": "You are logged in as " + current_user.email}

@router.post("/api/auth/refresh")
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")

    tokens = Logic.refresh_tokens(refresh_token)
    update_tokens(tokens, response)

    response.status_code = 200

    return {"message": "Tokens refreshed successfully"}