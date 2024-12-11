from abc import ABC, abstractmethod

from typing import Dict

from api.router.models import LoginRequest
from api.router.models import SignupRequest

from api.storage.models import User

from fastapi import Response

class LogicInterface(ABC):

    @staticmethod
    @abstractmethod
    def handle_login(login_data: LoginRequest) -> Dict[str, str]:
        """
        Authenticates the user by verifying their email and password, and generates an access token if successful.

        Args:
            login_data (LoginRequest): The login data containing the user's email and password.

        Raises:
            HTTPException: If the email is not found or the password is incorrect, an HTTPException is raised with status code 401.

        Returns:
            str: The generated JWT access token.
        """
        pass

    @staticmethod
    @abstractmethod
    def handle_signup(signup_data: SignupRequest) -> Dict[str, str]:
        """
        Handles the signup request by creating a new user and returning an access token.

        Args:
            signup_data (SignupRequest): The signup request data.

        Raises:
            HTTPException: If the email was found with the same user type, an HTTPException is raised with status code 400.
        
        Returns:
            str: The JWT access token.
        """
        pass

    @staticmethod
    @abstractmethod
    def handle_logout(cls) -> None:
        """
        Logs out the user by invalidating the current access token.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_current_user(token: str) -> User:
        """
        Verifies the token and returns the user data.

        Args:
            token (str): The JWT access token.

        Returns:
            User: The user data.
        """
        pass

    @staticmethod
    @abstractmethod
    def refresh_tokens(refresh_token: str) -> Dict[str, str]:
        """
        Refreshes the access and refresh tokens using the provided refresh token.

        Args:
            refresh_token (str): The refresh token.

        Returns:
            Dict[str, str]: A dictionary containing the new access and refresh tokens.
        """
        pass