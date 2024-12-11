from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional, Dict

from api.auth.models import TokenData
from api.common.utils import Utils

class AuthInterface(ABC):

    @staticmethod
    @abstractmethod
    def serialize_token_data(token_data: TokenData) -> dict:
        """
        Serializes the token data into a dictionary.

        Args:
            token_data (TokenData): The token data to serialize.

        Returns:
            dict: The serialized token data.
        """
        pass
    
    @staticmethod
    @abstractmethod
    def deserialize_token(token: dict) -> TokenData:
        """
        Deserializes the token data from a dictionary.

        Args:
            token (dict): The dictionary containing the token data.

        Raises:
            ValidationError: If the token data is invalid.

        Returns:
            TokenData: The deserialized token data.
        """
        pass

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
    def refresh_tokens(refresh_token: str) -> Dict[str, str]:
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