from fastapi import HTTPException
from jose import JWTError

from api.auth.auth_service import AuthService
from api.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES

from api.exceptions import UserAlreadyExistsError
from api.exceptions import UserNotFoundError

from api.logic.logic_interface import LogicInterface

from api.router.models import LoginRequest
from api.router.models import SignupRequest

from api.storage.storage_service import StorageService

class Logic(LogicInterface):

    @staticmethod
    def handle_login(login_data: LoginRequest) -> str:
        try:
            user = StorageService.find_one_user({"email": login_data.email, "userType": login_data.userType})
        except UserNotFoundError:
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        
        if not AuthService.verify_password(login_data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        
        token = AuthService.create_access_token(data={"sub": login_data.email, "userType": login_data.userType})
        
        return token

    @staticmethod
    def handle_signup(signup_data: SignupRequest) -> str:

        hashed_password = AuthService.hash_password(signup_data.password)

        try:
            _ = StorageService.create_user(
                email=signup_data.email,
                name=signup_data.name,
                password_hash=hashed_password,
                userType=signup_data.userType
            )
        except UserAlreadyExistsError as e:
            raise HTTPException(status_code=400, detail=str(e))  # to change to 409
        
        token = AuthService.create_access_token(data={"sub": signup_data.email, "userType": signup_data.userType})

        return token
    
    @staticmethod
    def handle_logout(cls):
        pass

    @staticmethod
    def handle_token(token: str, response):

        response.set_cookie(
            key="auth_token",
            value=token,
            httponly=True,  # Prevent JavaScript access
            secure=True,    # Use HTTPS in production
            samesite="strict",  # CSRF protection
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Token expiration
        )

    @staticmethod
    def get_current_user(token: str):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = AuthService.verify_token(token)
        except JWTError:
            raise credentials_exception
        
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        user = StorageService.find_one_user({"email": email, "userType": payload.get("userType")})
        if user is None:
            raise credentials_exception
        return user