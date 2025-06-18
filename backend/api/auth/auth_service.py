from datetime import datetime, timedelta, timezone

import bcrypt
from api.auth.auth_interface import AuthInterface
from api.auth.models import TokenData, TokenPair
from api.common.utils import Utils
from api.config import settings
from jose import jwt

JWT_SECRET_KEY = settings.jwt_secret_key
JWT_ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_SECRET_KEY = settings.refresh_token_secret_key
REFRESH_TOKEN_EXPIRE_MINUTES = settings.refresh_token_expire_minutes

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
    def create_access_token(token_data: TokenData, token_version: int = 0, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
        Utils.validate_non_empty(token_data=token_data)
        to_encode = token_data.model_dump()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({
            "exp": expire,
            "type": "access",
            "token_version": token_version
        })
        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def create_refresh_token(token_data: TokenData, token_version: int = 0, expires_delta: timedelta = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)) -> str:
        Utils.validate_non_empty(token_data=token_data)
        to_encode = token_data.model_dump()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({
            "exp": expire,
            "type": "refresh",
            "token_version": token_version
        })
        return jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def verify_token(token: str, is_refresh: bool = False) -> TokenData:
        Utils.validate_non_empty(token=token)
        secret_key = REFRESH_TOKEN_SECRET_KEY if is_refresh else JWT_SECRET_KEY
        payload = jwt.decode(token, secret_key, algorithms=[JWT_ALGORITHM])
        
        # Optional: Add type validation if needed
        if is_refresh and payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")
        if not is_refresh and payload.get("type") != "access":
            raise ValueError("Invalid access token")
        
        # Create a copy of the payload to modify
        token_payload = payload.copy()
        
        # Remove time-related fields
        token_payload.pop("exp")
        token_payload.pop("type")
        
        # Ensure token_version is preserved
        if "token_version" in payload:
            token_payload["token_version"] = payload["token_version"]
        
        return TokenData(**token_payload)

    @staticmethod
    def refresh_tokens(refresh_token: str) -> TokenPair:
        # Verify refresh token
        token_data = AuthService.verify_token(refresh_token, is_refresh=True)
        
        # Generate new access and refresh tokens
        new_access_token = AuthService.create_access_token(token_data)
        new_refresh_token = AuthService.create_refresh_token(token_data)
        
        return TokenPair(
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )

    @staticmethod
    def create_password_reset_token(token_data: TokenData, token_version: int = 0, expires_delta: timedelta = timedelta(hours=1)) -> str:
        """
        Create a password reset token with a specific expiration time
        """
        Utils.validate_non_empty(token_data=token_data)
        to_encode = token_data.model_dump()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({
            "exp": expire,
            "type": "password_reset",
            "token_version": token_version
        })
        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def verify_password_reset_token(token: str) -> TokenData:
        """
        Verify a password reset token and return the token data
        """
        Utils.validate_non_empty(token=token)
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            
            # Validate token type
            if payload.get("type") != "password_reset":
                raise ValueError("Invalid password reset token")
            
            # Create a copy of the payload to modify
            token_payload = payload.copy()
            
            # Remove time-related fields
            token_payload.pop("exp")
            token_payload.pop("type")
            
            # Preserve any additional fields like token_version if present
            return TokenData(**token_payload)
        except jwt.JWTError as e:
            raise ValueError("Invalid or expired password reset token")