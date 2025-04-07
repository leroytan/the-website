from api.auth.config import (ACCESS_TOKEN_EXPIRE_MINUTES,
                             REFRESH_TOKEN_EXPIRE_MINUTES)
from api.logic.logic import Logic
from api.storage.models import User
from fastapi import Request, Response


class RouterAuthUtils:

    @staticmethod
    def clear_tokens(response: Response) -> None:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

    @staticmethod
    def update_tokens(tokens: dict[str, str], response: Response) -> None:
        """
        Update the response with new access and refresh tokens.
        This method sets the tokens as HTTP-only cookies in the response,
        which helps prevent JavaScript access and enhances security.
        Args:
            tokens (dict): A dictionary containing the new access and refresh tokens.
            response (Response): The response object to update with the new tokens.
        """
        response.set_cookie(
            key="access_token",
            value=tokens["access_token"],
            httponly=True,  # Prevent JavaScript access
            secure=True,    # Use HTTPS in production
            samesite="strict",  # CSRF protection
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Token expiration
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh_token"],
            httponly=True,  # Prevent JavaScript access
            secure=True,    # Use HTTPS in production
            samesite="strict",  # CSRF protection
            max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,  # Token expiration
        )


    @staticmethod
    async def get_current_user(request: Request) -> User:
        token = request.cookies.get("access_token")
        user = Logic.get_current_user(token)
        return user
