from api.router.models import (
    LoginRequest,
    SignupRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from api.logic.logic import Logic
from api.router.auth_utils import RouterAuthUtils
from fastapi import Depends
from api.storage.models import User
from api.storage.models import User
from fastapi import APIRouter, Depends, Request, Response, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.post("/api/auth/login")
async def login(
    login_request: LoginRequest,
    response: Response,
    _ = Depends(RouterAuthUtils.assert_logged_out)
):
    """
    Handles user login by validating the provided credentials and generating 
    an authentication token. The token is then set as an HTTP-only cookie in 
    the response for secure and persistent access.

    Args:
        request (Request): The request object containing the login data
        response (Response): The response object used to set the authentication 
                              token as a secure HTTP-only cookie.

    Raises:
        HTTPException: If the login credentials are invalid or the login process 
                        fails, an HTTP error is raised with an appropriate status code.
    """

    tokens = Logic.handle_login(login_data=login_request)
    RouterAuthUtils.update_tokens(tokens, response)

    return {"message": "Logged in successfully"}

@router.post("/api/auth/signup")
async def signup(
    signup_request: SignupRequest,
    response: Response,
    _ = Depends(RouterAuthUtils.assert_logged_out)
):
    """
    Handles user registration by processing the provided signup data, 
    creating a new user account, and generating an authentication token. 
    The token is then set as an HTTP-only cookie in the response for secure 
    and persistent access.

    Args:
        request (Request): The request object containing the signup data
        response (Response): The response object used to set the authentication 
                              token as a secure HTTP-only cookie.

    Raises:
        HTTPException: If the signup process fails (e.g., due to validation errors 
                        or a conflict with existing accounts), an HTTP error is 
                        raised with an appropriate status code.
    """
    
    tokens = Logic.handle_signup(signup_request)
    RouterAuthUtils.update_tokens(tokens, response)

    response.status_code = 201

    return {"message": "Signed up successfully"}
    

@router.post("/api/auth/logout")
async def logout(response: Response, _ = Depends(RouterAuthUtils.assert_not_logged_out)):
    RouterAuthUtils.clear_tokens(response)
    return {"message": "Logged out successfully"}

@router.get("/api/protected")
async def protected_route(user: User = Depends(RouterAuthUtils.get_current_user)):
    # Test route for authentication
    return {"message": "This is a protected route", "user_id": user.id}

@router.post("/api/auth/refresh")
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")

    tokens = Logic.refresh_tokens(refresh_token)
    RouterAuthUtils.update_tokens(tokens, response)

    return {"message": "Tokens refreshed successfully"}

@router.get("/api/auth/check")
async def check(_: User = Depends(RouterAuthUtils.get_current_user)):
    return {"message": "Valid token"}

@router.get("/api/auth/me")
async def me(user: User = Depends(RouterAuthUtils.get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
    }

@router.post("/api/auth/forgot-password")
async def forgot_password(
    request: Request,
    forgot_password_request: ForgotPasswordRequest,
):
    """
    Initiate password reset process by sending a reset link to the user's email.
    
    Args:
        forgot_password_request (ForgotPasswordRequest): Contains the email address
        for password reset.
    
    Returns:
        dict: A message indicating the status of the password reset request.
    """
    # Use the request's origin to generate the reset link
    origin = request.headers.get("origin", "http://localhost:3000")
    return Logic.forgot_password(origin, forgot_password_request)

@router.post("/api/auth/reset-password")
async def reset_password(
    reset_password_request: ResetPasswordRequest,
):
    """
    Complete password reset by validating the reset token and updating the password.
    
    Args:
        reset_password_request (ResetPasswordRequest): Contains the reset token
        and new password.
    
    Returns:
        dict: A message indicating the success of the password reset.
    """
    return Logic.reset_password(reset_password_request)
