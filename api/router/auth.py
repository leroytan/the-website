from fastapi import Depends, Response, APIRouter
from fastapi.security import OAuth2PasswordBearer

from api.router.models import LoginRequest
from api.router.models import SignupRequest

from api.logic.logic import Logic

router = APIRouter()

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
    user = Logic.get_current_user(token)
    return user

@router.post("/api/auth/login")
async def login(login_data: LoginRequest, response: Response):
    """
    Handles user login by validating the provided credentials and generating 
    an authentication token. The token is then set as an HTTP-only cookie in 
    the response for secure and persistent access.

    Args:
        login_data (LoginRequest): The login credentials provided by the user, 
                                    including username/email and password.
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

    token = Logic.handle_login(login_data=login_data)

    Logic.handle_token(token, response)

    response.status_code = 200

    return "yay all is good" # not necessary

@router.post("/api/auth/signup")
async def signup(signup_data: SignupRequest, response: Response):
    """
    Handles user registration by processing the provided signup data, 
    creating a new user account, and generating an authentication token. 
    The token is then set as an HTTP-only cookie in the response for secure 
    and persistent access.

    Args:
        signup_data (SignupRequest): The registration data provided by the 
                                      user, including necessary details like 
                                      username, email, and password.
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
    
    token = Logic.handle_signup(signup_data=signup_data)

    Logic.handle_token(token, response)

    response.status_code = 201

    return "yay all is good"
    

@router.post("/api/auth/logout")
async def logout(response: Response):
    response.delete_cookie("auth_token")
    return {"message": "Logged out successfully"}

@router.get("/api/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "You are logged in as " + current_user["email"]}