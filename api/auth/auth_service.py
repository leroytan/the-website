import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt
from typing import Optional, Dict

from api.auth.auth_interface import AuthInterface
from api.auth.config import (
    JWT_SECRET_KEY, 
    REFRESH_TOKEN_SECRET_KEY, 
    JWT_ALGORITHM, 
    ACCESS_TOKEN_EXPIRE_MINUTES, 
    REFRESH_TOKEN_EXPIRE_MINUTES
)

from api.common.utils import Utils

class AuthService(AuthInterface):

    @staticmethod
    def hash_password(password: str) -> str:
        Utils.validate_non_empty(password=password)
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        Utils.validate_non_empty(
            plain_password=plain_password, 
            hashed_password=hashed_password
        )
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        Utils.validate_non_empty(data=data)
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        Utils.validate_non_empty(data=data)
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def verify_token(token: str, is_refresh: bool = False) -> Dict:
        Utils.validate_non_empty(token=token)
        secret_key = REFRESH_TOKEN_SECRET_KEY if is_refresh else JWT_SECRET_KEY
        payload = jwt.decode(token, secret_key, algorithms=[JWT_ALGORITHM])
        
        # Optional: Add type validation if needed
        if is_refresh and payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")
        if not is_refresh and payload.get("type") != "access":
            raise ValueError("Invalid access token")
        
        return payload

    @staticmethod
    def refresh_tokens(refresh_token: str) -> Dict[str, str]:
        # Verify refresh token
        refresh_payload = AuthService.verify_token(refresh_token, is_refresh=True)
        
        # Extract user data for new tokens
        token_data = {key: value for key, value in refresh_payload.items() 
                    if key not in ["exp", "type"]}
        
        # Generate new access and refresh tokens
        new_access_token = AuthService.create_access_token(token_data)
        new_refresh_token = AuthService.create_refresh_token(token_data)
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }