from api.auth.auth_service import AuthService
from api.auth.models import TokenData, TokenPair
from api.common.models import LoginRequest, SignupRequest
from api.exceptions import UserAlreadyExistsError, UserNotFoundError
from api.storage.models import (Base, Level, Subject, Tutor, TutorLevel,
                                TutorSubject, User)
from api.storage.storage_service import StorageService
from fastapi import HTTPException
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class Logic:

    @staticmethod
    def handle_login(login_data: LoginRequest) -> TokenPair:
        with Session(StorageService.engine) as session:
            # Check if user exists
            user = StorageService.find(session, {"email": login_data.email}, User, find_one=True)
            if not user or not AuthService.verify_password(login_data.password, user.passwordHash):
                raise HTTPException(status_code=401, detail="Incorrect email or password")
    
        token_data = TokenData(email=login_data.email)
        
        access_token = AuthService.create_access_token(token_data)
        refresh_token = AuthService.create_refresh_token(token_data)

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token
        )

    @staticmethod
    def handle_signup(signup_data: SignupRequest) -> TokenPair:

        hashed_password = AuthService.hash_password(signup_data.password)

        with Session(StorageService.engine) as session:
            try:
                StorageService.insert(
                    session, 
                    User(
                        email=signup_data.email,
                        name=signup_data.name,
                        passwordHash=hashed_password,
                    )
                )
            except IntegrityError as e:
                raise HTTPException(status_code=409, detail="User already exists")
            
            token_data = TokenData(email=signup_data.email)
            
            access_token = AuthService.create_access_token(token_data)
            refresh_token = AuthService.create_refresh_token(token_data)

            return TokenPair(
                access_token=access_token,
                refresh_token=refresh_token
            )

    @staticmethod
    def get_current_user(access_token: str) -> User:
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = AuthService.verify_token(access_token)

            if payload.email is None:
                raise credentials_exception
            
            with Session(StorageService.engine) as session:
                user = StorageService.find(session, {"email": payload.email}, User, find_one=True)
                if user is None:
                    raise credentials_exception
                return user
        
        except (JWTError, ValueError, ValidationError) as e:
            raise credentials_exception

    
    @staticmethod
    def refresh_tokens(refresh_token: str) -> TokenPair:
        try:
            return AuthService.refresh_tokens(refresh_token)
        except (JWTError, ValueError, ValidationError) as e:
            raise HTTPException(status_code=401, detail="Invalid refresh token") 