from datetime import datetime, timedelta, timezone
import httpx
import bcrypt
from api.auth.models import TokenData, TokenPair
from api.common.utils import Utils
from api.config import settings
from jose import jwt
from api.storage.storage_service import StorageService
from api.storage.models import User

JWT_SECRET_KEY = settings.jwt_secret_key
JWT_ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_SECRET_KEY = settings.refresh_token_secret_key
REFRESH_TOKEN_EXPIRE_MINUTES = settings.refresh_token_expire_minutes

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

class AuthService:
    
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
    def create_access_token(token_data: TokenData, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
        Utils.validate_non_empty(token_data=token_data)
        to_encode = token_data.model_dump()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({
            "exp": expire,
            "type": "access",
        })
        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def create_refresh_token(token_data: TokenData, expires_delta: timedelta = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)) -> str:
        Utils.validate_non_empty(token_data=token_data)
        to_encode = token_data.model_dump()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({
            "exp": expire,
            "type": "refresh",
        })
        return jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    @staticmethod
    def create_token_pair(token_data: TokenData) -> TokenPair:
        return TokenPair(
            access_token=AuthService.create_access_token(token_data=token_data),
            refresh_token=AuthService.create_refresh_token(token_data=token_data),
        )

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
        
        return TokenData(**token_payload)

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

    @staticmethod
    def verify_password_reset_token_for_validation(token: str) -> TokenData:
        """
        Verify a password reset token for validation purposes (no expiration check here).
        This is used to check if the token is syntactically valid and was issued by us.
        """
        Utils.validate_non_empty(token=token)
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM], options={"verify_exp": False})
            
            # Validate token type
            if payload.get("type") != "password_reset":
                raise ValueError("Invalid password reset token type")
            
            # Create a copy of the payload to modify
            token_payload = payload.copy()
            
            # Remove time-related fields
            token_payload.pop("exp")
            token_payload.pop("type")
            
            # Preserve any additional fields like token_version if present
            return TokenData(**token_payload)
        except jwt.JWTError as e:
            raise ValueError("Invalid password reset token format or signature")

    @staticmethod
    async def authenticate_google_user(code: str) -> TokenPair:
        # Exchange authorization code for tokens
        token_response = await httpx.AsyncClient().post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.google_redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        token_response.raise_for_status()
        google_tokens = token_response.json()
        access_token = google_tokens["access_token"]

        # Fetch user info from Google
        user_info_response = await httpx.AsyncClient().get(
            GOOGLE_USER_INFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_info_response.raise_for_status()
        google_user_info = user_info_response.json()

        google_id = google_user_info["sub"]
        email = google_user_info["email"]
        name = google_user_info.get("name", email.split("@")[0]) # Default name if not provided

        # Check if user exists by google_id
        user = StorageService.get_user_by_google_id(google_id)
        if user:
            # User exists with google_id, log them in
            token_data = TokenData(email=user.email, token_version=user.token_version)
            return AuthService.create_token_pair(token_data=token_data)
        # Check if user exists by email (for linking accounts)
        user = StorageService.get_user_by_email(email)
        if user:
            # User exists with email, link google_id and log them in
            StorageService.update_user_google_id(user.id, google_id)
            token_data = TokenData(email=user.email, token_version=user.token_version)
            return AuthService.create_token_pair(token_data=token_data)

        # If no user found, create a new one
        new_user = StorageService.create_user(
            name=name,
            email=email,
            password_hash=None, # No password for Google-only accounts
            google_id=google_id,
            intends_to_be_tutor=False # Default, can be changed later
        )
        token_data = TokenData(email=new_user.email, token_version=new_user.token_version)
        return AuthService.create_token_pair(token_data=token_data)