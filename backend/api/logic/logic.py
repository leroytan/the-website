from api.auth.auth_service import AuthService
from api.auth.models import TokenData
from api.common.models import LoginRequest, SignupRequest
from api.exceptions import UserAlreadyExistsError, UserNotFoundError
from api.logic.logic_interface import LogicInterface
from api.storage.models import (Base, Level, Subject, Tutor, TutorLevel,
                                TutorSubject, User)
from api.storage.storage_service import StorageService
from fastapi import HTTPException
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session


class Logic(LogicInterface):

    @staticmethod
    def handle_login(login_data: LoginRequest) -> dict[str, str]:
        with Session(StorageService.engine) as session:
            # Check if user exists
            user = StorageService.find(session, {"email": login_data.email, "userType": login_data.userType}, User, find_one=True)
            if not user:
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

        CurrentUser = User

        with Session(StorageService.engine) as session:
            if StorageService.find(session, {"email": signup_data.email, "userType": signup_data.userType}, User, find_one=True):
                raise HTTPException(status_code=400, detail="User already exists")  # TODO: change to 409

            try:
                StorageService.create_user(
                    CurrentUser(
                        email=signup_data.email,
                        name=signup_data.name,
                        password_hash=hashed_password,
                    )
                )
            except UserAlreadyExistsError as e:
                raise HTTPException(status_code=400, detail="User already exists")  # TODO: change to 409
            
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
        
        with Session(StorageService.engine) as session:
            user = StorageService.find(session, {"email": email, "userType": userType}, User, find_one=True)
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