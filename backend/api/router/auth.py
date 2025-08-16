import base64
import json
from urllib.parse import quote

from api.auth.models import TokenPair
from api.router.models import (
    LoginRequest,
    SignupRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    VerifyPasswordResetTokenRequest,
    EmailConfirmationRequest
)
from api.logic.logic import Logic
from api.router.auth_utils import RouterAuthUtils
from api.storage.models import User
from api.storage.models import User
from fastapi import APIRouter, Depends, Request, Response, HTTPException
from fastapi.responses import RedirectResponse
from api.config import settings

router = APIRouter()

@router.get("/api/auth/google/login")
async def google_login(request: Request):
    """
    Redirects to Google's OAuth consent screen for login/signup.
    """
    # Get the origin from the request
    origin = request.headers.get("origin") or request.headers.get("referer")
    origin = origin.rstrip('/')

    # Create state parameter with origin information
    state_data = {
        "origin": origin,
        # You can add other data here if needed
        # "timestamp": int(time.time()),
        # "user_id": user_id if available
    }
    
    # Encode the state data (base64 encode JSON for safety)
    state = base64.urlsafe_b64encode(
        json.dumps(state_data).encode()
    ).decode().rstrip('=')  # Remove padding for URL safety

    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"response_type=code&"
        f"client_id={settings.google_client_id}&"
        f"redirect_uri={settings.google_redirect_uri}&"
        f"scope=openid%20email%20profile&"
        f"access_type=offline&"
        f"prompt=consent&"
        f"state={quote(state)}"
    )
    return RedirectResponse(google_auth_url)

@router.get("/api/auth/google/callback")
async def google_callback(code: str = None, error: str = None, state: str = None):
    """
    Handles the callback from Google OAuth, exchanges the code for tokens,
    and logs in/signs up the user.
    """
    if error:
        raise HTTPException(status_code=400, detail=f"Google OAuth error: {error}")
    
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code missing")
    
    # Decode the state parameter to get the origin
    origin = None
    if state:
        try:
            # Add padding back for base64 decoding
            padded_state = state + '=' * (4 - len(state) % 4)
            state_data = json.loads(base64.urlsafe_b64decode(padded_state).decode())
            origin = state_data.get("origin")
        except Exception as e:
            # Log the error but don't fail the authentication
            print(f"Failed to decode state parameter: {e}")

    try:
        tokens = await Logic.handle_google_login_signup(code)

        # Use the origin from state if available, otherwise fall back to default
        redirect_url = origin or settings.frontend_domain
        
        # Encode tokens and their cookie parameters ONLY for Google login
        tokens_dict = {
            "access_token": tokens.access_token,
            "refresh_token": tokens.refresh_token,
            "access_cookie_params": RouterAuthUtils._get_cookie_params(redirect_url),
            "refresh_cookie_params": RouterAuthUtils._get_cookie_params(redirect_url)
        }
        
        # Modify cookie params to not be HTTP-only for frontend
        tokens_dict["access_cookie_params"]["httponly"] = False
        tokens_dict["refresh_cookie_params"]["httponly"] = False
        
        encoded_tokens = base64.urlsafe_b64encode(
            json.dumps(tokens_dict).encode()
        ).decode().rstrip('=')
        
        return RedirectResponse(url=f"{redirect_url}/login?tokens={encoded_tokens}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Google login failed: {str(e)}")

@router.post("/api/auth/login")
async def login(
    login_request: LoginRequest,
    request: Request,
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
    origin = request.headers.get("origin") or request.headers.get("referer") or settings.frontend_domain
    RouterAuthUtils.update_tokens(tokens, response, origin)

    return {"message": "Logged in successfully"}

@router.post("/api/auth/signup")
async def signup(
    signup_request: SignupRequest,
    request: Request,
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
    
    origin = request.headers.get("origin") or request.headers.get("referer") or settings.frontend_domain
    result = Logic.handle_signup(signup_request, origin)
    
    # Check if result is a token pair (for verified users)
    if isinstance(result, TokenPair):
        # User is verified (e.g., @example.com), set tokens and log them in
        RouterAuthUtils.update_tokens(result, response, origin)
        response.status_code = 201
        return {"message": "Signed up successfully"}
    
    # For all other cases (waitlist, email verification needed), just return the message
    response.status_code = 201
    return result
    

@router.post("/api/auth/logout")
async def logout(request: Request, response: Response, _ = Depends(RouterAuthUtils.assert_not_logged_out)):
    origin = request.headers.get("origin") or request.headers.get("referer") or settings.frontend_domain
    RouterAuthUtils.clear_tokens(response, origin)
    return {"message": "Logged out successfully"}

@router.get("/api/protected")
async def protected_route(user: User = Depends(RouterAuthUtils.get_current_user)):
    # Test route for authentication
    return {"message": "This is a protected route", "user_id": user.id}

@router.post("/api/auth/refresh")
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")

    tokens = Logic.refresh_tokens(refresh_token)
    origin = request.headers.get("origin") or request.headers.get("referer") or settings.frontend_domain
    RouterAuthUtils.update_tokens(tokens, response, origin)

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
    origin = request.headers.get("origin") or request.headers.get("referer") or settings.frontend_domain
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

@router.post("/api/auth/verify-password-reset-token")
async def verify_password_reset_token(
    verify_password_reset_token_request: VerifyPasswordResetTokenRequest,
):
    """
    Verify a password reset token for validation purposes.
    
    Args:
        verify_password_reset_token_request (VerifyPasswordResetTokenRequest): Contains the reset token to verify.
    
    Returns:
        dict: A message indicating the validity of the reset token.
    """
    return Logic.verify_password_reset_token(verify_password_reset_token_request)

@router.post("/api/auth/confirm-email")
async def confirm_email(
    confirmation_request: EmailConfirmationRequest,
):
    """
    Confirm user email by validating the confirmation token.
    
    Args:
        confirmation_request (EmailConfirmationRequest): Contains the confirmation token.
    
    Returns:
        dict: A message indicating the success of email confirmation.
    """
    return Logic.confirm_email(confirmation_request)

@router.post("/api/auth/resend-confirmation-email")
async def resend_confirmation_email(
    request: Request,
    email: str,
):
    """
    Resend email confirmation link to the user's email address.
    
    Args:
        email (str): The email address to resend confirmation to.
    
    Returns:
        dict: A message indicating the status of the confirmation email request.
    """
    # Use the request's origin to generate the confirmation link
    origin = request.headers.get("origin") or request.headers.get("referer") or settings.frontend_domain
    return Logic.resend_confirmation_email(email, origin)
