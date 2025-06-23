from collections.abc import Callable
from datetime import datetime, timedelta, timezone

from api.auth.auth_service import AuthService
from api.auth.models import TokenData, TokenPair
from api.router.models import (
    LoginRequest,
    SignupRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from api.storage.models import User
from api.storage.storage_service import StorageService
from api.services.email_service import GmailEmailService
from fastapi import HTTPException, Request
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select
from api.config import settings

class Logic:

    @staticmethod
    def handle_login(login_data: LoginRequest) -> TokenPair:
        with Session(StorageService.engine) as session:
            # Check if user exists
            user = session.execute(select(User).filter_by(email=login_data.email)).scalar_one_or_none()
            if not user or not user.password_hash or not AuthService.verify_password(login_data.password, user.password_hash):
                raise HTTPException(status_code=401, detail="Incorrect email or password. Did you previously sign in with Google?")
    
        token_data = TokenData(email=login_data.email)
        
        access_token = AuthService.create_access_token(token_data, token_version=user.token_version)
        refresh_token = AuthService.create_refresh_token(token_data, token_version=user.token_version)

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token
        )

    @staticmethod
    def handle_signup(signup_data: SignupRequest) -> TokenPair:

        signup_data_dict = signup_data.model_dump()
        signup_data_dict.pop("password")

        hashed_password = AuthService.hash_password(signup_data.password)
        signup_data_dict["password_hash"] = hashed_password

        with Session(StorageService.engine) as session:
            try:
                user = User(**signup_data_dict)
                session.add(user)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise HTTPException(status_code=409, detail="User already exists")
            
            token_data = TokenData(email=signup_data.email)
            
            access_token = AuthService.create_access_token(token_data, token_version=user.token_version)
            refresh_token = AuthService.create_refresh_token(token_data, token_version=user.token_version)

            return TokenPair(
                access_token=access_token,
                refresh_token=refresh_token
            )

    @staticmethod
    def get_current_user(access_token: str, credentials_exception: HTTPException) -> User:
        try:
            if access_token is None:
                raise credentials_exception
            payload = AuthService.verify_token(access_token)

            if payload.email is None:
                raise credentials_exception
            
            with Session(StorageService.engine) as session:
                user = session.execute(select(User).filter_by(email=payload.email)).scalar_one_or_none()
                if user is None:
                    raise credentials_exception
                
                # Validate token version
                if payload.token_version != user.token_version:
                    credentials_exception.detail = "Token version mismatch. Please log in again."
                    raise credentials_exception
                
                return user
        
        except (JWTError, ValueError, ValidationError) as e:
            raise credentials_exception

    @staticmethod
    def refresh_tokens(refresh_token: str) -> TokenPair:
        try:
            # Verify the refresh token and get the token data
            token_data = AuthService.verify_token(refresh_token, is_refresh=True)
            
            # Find the user to get the current token_version
            with Session(StorageService.engine) as session:
                user = session.execute(select(User).filter_by(email=token_data.email)).scalar_one_or_none()
                if not user:
                    raise HTTPException(status_code=401, detail="User not found")
                
                # Generate new tokens with the current token_version
                new_access_token = AuthService.create_access_token(token_data, token_version=user.token_version)
                new_refresh_token = AuthService.create_refresh_token(token_data, token_version=user.token_version)
                
                return TokenPair(
                    access_token=new_access_token,
                    refresh_token=new_refresh_token
                )
        except (JWTError, ValueError, ValidationError) as e:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
    @staticmethod
    def create_assert_user_authorized(user_id: int) -> Callable[[int], None]:
        def assert_user_authorized(correct_id: int) -> None:
            if user_id != correct_id:
                raise HTTPException(status_code=403, detail="Unauthorized action")
        return assert_user_authorized

    @staticmethod
    def forgot_password(origin: str, forgot_password_request: ForgotPasswordRequest) -> dict:
        """
        Initiate password reset process by generating a reset token
        """
        with Session(StorageService.engine) as session:
            # Find user by email
            user = session.execute(select(User).filter_by(email=forgot_password_request.email)).scalar_one_or_none()
            
            # Always return success to prevent email enumeration
            if not user:
                return {"message": "If the email is registered, a reset link has been sent."}
            
            # Generate a secure reset token (JWT)
            reset_token = AuthService.create_password_reset_token(
                TokenData(email=user.email),
                token_version=user.token_version
            )
            
            # Store the reset token and its expiration on the user
            user.password_reset_token = reset_token
            user.password_reset_token_expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
            
            # Commit changes
            session.add(user)
            session.commit()
            
            reset_link = GmailEmailService.create_reset_link(reset_token, origin)
            GmailEmailService.send_password_reset_email(
                recipient_email=forgot_password_request.email,
                reset_link=reset_link
            )
            
            return {"message": "If the email is registered, a reset link has been sent."}

    @staticmethod
    def reset_password(reset_password_request: ResetPasswordRequest) -> dict:
        """
        Complete password reset by validating reset token and updating password
        """
        with Session(StorageService.engine) as session:
            try:
                # Verify the reset token
                payload = AuthService.verify_password_reset_token(reset_password_request.reset_token)
                
                # Find the user
                user = session.execute(select(User).filter_by(email=payload.email)).scalar_one_or_none()
                if not user:
                    raise HTTPException(status_code=404, detail="User not found")
                
                # Validate token against stored token and expiration
                if (user.password_reset_token != reset_password_request.reset_token or
                    user.password_reset_token_expires_at < datetime.now(timezone.utc)):
                    raise HTTPException(status_code=400, detail="Invalid or expired reset token")
                
                # Update user's password
                user.password_hash = AuthService.hash_password(reset_password_request.new_password)
                
                # Increment token version to invalidate existing tokens
                user.token_version += 1
                
                # Clear the reset token
                user.password_reset_token = None
                user.password_reset_token_expires_at = None
                
                # Commit changes
                session.add(user)
                session.commit()
                
                return {
                    "message": "Password successfully updated",
                    "token_version": user.token_version
                }
            
            except (JWTError, ValueError) as e:
                raise HTTPException(status_code=400, detail="Invalid reset token")

    @staticmethod
    async def handle_google_login_signup(code: str) -> TokenPair:
        """
        Handles Google OAuth login/signup flow.
        """
        try:
            tokens = await AuthService.authenticate_google_user(code)
            return tokens
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Google authentication failed: {str(e)}")