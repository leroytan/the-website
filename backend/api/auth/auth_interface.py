from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional

from api.auth.models import TokenData
from api.common.utils import Utils


class AuthInterface(ABC):

    @staticmethod
    @abstractmethod
    def hash_password(password: str) -> str:
        """
        Hashes the provided password using bcrypt.

        Args:
            password (str): The plain text password to be hashed.

        Returns:
            str: The hashed password as a string.
        """
        pass

    @staticmethod
    @abstractmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Checks if the provided plain text password matches the hashed password.

        Args:
            plain_password (str): The plain text password to be checked.
            hashed_password (str): The hashed password to be checked against.

        Returns:
            bool: True if the plain password matches the hashed password, False otherwise.
        """
        pass

    @staticmethod
    @abstractmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Creates an access token using the provided data and optional expiration time.

        Args:
            data (dict): A dictionary of data to encode into the JWT.
            expires_delta (Optional[timedelta], optional): The expiration time for the token.
                If None, the token will expire in 15 minutes. Defaults to None.

        Returns:
            str: The encoded JWT access token.
        """
        pass

    @staticmethod
    @abstractmethod
    def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Creates an refresh token using the provided data and optional expiration time.

        Args:
            data (dict): A dictionary of data to encode into the JWT.
            expires_delta (Optional[timedelta], optional): The expiration time for the token.
                If None, the token will expire in 15 minutes. Defaults to None.

        Returns:
            str: The encoded JWT access token.
        """
        pass 

    @staticmethod
    @abstractmethod
    def verify_token(token: str):
        """
        Verifies the JWT token and returns its payload.

        Args:
            token (str): The JWT token to verify.

        Raises:
            jwt.JWTError: If the token is invalid or expired.

        Returns:
            dict: The payload of the decoded JWT token.
        """
        pass

    @staticmethod
    @abstractmethod
    def refresh_tokens(refresh_token: str) -> dict[str, str]:
        """
        Refreshes the access and refresh tokens using the provided refresh token.

        Args:
            refresh_token (str): The refresh token to use for token refresh.

        Raises:
            jwt.JWTError: If the token is invalid or expired.
            pydantic.ValidationError: If the token data is in the wrong format.

        Returns:
            dict: A dictionary containing the new access and refresh tokens.
        """
        pass

    @staticmethod
    @abstractmethod
    def authenticate_google_user(code: str) -> dict[str, str]:
        """
        Authenticates a user using Google OAuth2 authorization code.

        Args:
            code (str): The authorization code received from Google.

        Returns:
            dict: A dictionary containing the application's access and refresh tokens.
        """
        pass

    @staticmethod
    @abstractmethod
    def create_password_reset_token(token_data: TokenData, token_version: int = 0, expires_delta: Optional[timedelta] = None) -> str:
        """
        Creates a password reset token.
        """
        pass

    @staticmethod
    @abstractmethod
    def verify_password_reset_token(token: str) -> TokenData:
        """
        Verifies a password reset token.
        """
        pass

    @staticmethod
    @abstractmethod
    def verify_password_reset_token_for_validation(token: str) -> TokenData:
        """
        Verifies a password reset token for validation purposes (no expiration check).
        """
        pass