from fastapi import HTTPException
from jose import JWTError

from pydantic import ValidationError

from api.auth.auth_service import AuthService

from api.exceptions import UserAlreadyExistsError
from api.exceptions import UserNotFoundError

from api.logic.logic_interface import LogicInterface

from api.router.models import LoginRequest
from api.router.models import SignupRequest

from api.storage.storage_service import StorageService
from api.storage.models import User

from api.auth.models import TokenData

class Logic(LogicInterface):

    @staticmethod
    def handle_login(login_data: LoginRequest) -> dict[str, str]:
        try:
            user = StorageService.find_one_user({"email": login_data.email, "userType": login_data.userType})
        except UserNotFoundError:
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        
        if not AuthService.verify_password(login_data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        
        token_data = TokenData(email=login_data.email, userType=login_data.userType)
        
        access_token = AuthService.create_access_token(token_data)
        refresh_token = AuthService.create_refresh_token(token_data)

        return {"access_token": access_token, "refresh_token": refresh_token}

    @staticmethod
    def handle_signup(signup_data: SignupRequest) -> dict[str, str]:

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
        
        token_data = TokenData(email=signup_data.email, userType=signup_data.userType)
        
        access_token = AuthService.create_access_token(token_data)
        refresh_token = AuthService.create_refresh_token(token_data)

        return {"access_token": access_token, "refresh_token": refresh_token}

    
    @staticmethod
    def handle_logout(cls):
        pass

    @staticmethod
    def get_current_user(token: str) -> User:
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = AuthService.verify_token(token)
        except JWTError:
            raise credentials_exception
        
        email = payload.email
        if email is None:
            raise credentials_exception
        
        userType = payload.userType
        if userType is None:
            raise credentials_exception
        
        user = StorageService.find_one_user({"email": email, "userType": userType})
        if user is None:
            raise credentials_exception
        return user
    
    @staticmethod
    def refresh_tokens(refresh_token: str) -> dict[str, str]:
        try:
            return AuthService.refresh_tokens(refresh_token)
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        except ValidationError:
            raise HTTPException(status_code=401, detail="Invalid refresh token format")    