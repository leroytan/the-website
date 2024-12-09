from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional

class AuthInterface(ABC):

    @classmethod
    @abstractmethod
    def hash_password(cls, password: str) -> str:
        """
        Hashes the provided password using bcrypt.

        Args:
            password (str): The plain text password to be hashed.

        Returns:
            str: The hashed password as a string.
        """
        pass

    @classmethod
    @abstractmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """
        Checks if the provided plain text password matches the hashed password.

        Args:
            plain_password (str): The plain text password to be checked.
            hashed_password (str): The hashed password to be checked against.

        Returns:
            bool: True if the plain password matches the hashed password, False otherwise.
        """
        pass

    @classmethod
    @abstractmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
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

    @classmethod
    @abstractmethod
    def verify_token(cls, token: str):
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