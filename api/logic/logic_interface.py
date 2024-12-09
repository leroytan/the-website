from abc import ABC, abstractmethod

from api.router.models import LoginRequest
from api.router.models import SignupRequest

from fastapi import Response

class LogicInterface(ABC):

    @classmethod
    @abstractmethod
    def handle_login(cls, login_data: LoginRequest) -> str:
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

    @classmethod
    @abstractmethod
    def handle_signup(cls, signup_data: SignupRequest) -> str:
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

    @classmethod
    @abstractmethod
    def handle_logout(cls):
        """
        Logs out the user by invalidating the current access token.
        """
        pass

    @classmethod
    @abstractmethod
    def handle_token(cls, token: str, response: Response):
        """
        Sets the token as an HTTP-only cookie in the response in-place.

        Args:
            token (str): The JWT access token.
            response (Response): The response object used to set the token as a cookie.

        Returns:
            None
        """
        pass

    @classmethod
    @abstractmethod
    def get_current_user(cls, token: str):
        """
        Verifies the token and returns the user data.

        Args:
            token (str): The JWT access token.

        Returns:
            User: The user data.
        """
        pass