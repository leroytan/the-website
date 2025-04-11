from api.auth.config import (ACCESS_TOKEN_EXPIRE_MINUTES,
                             REFRESH_TOKEN_EXPIRE_MINUTES)
from api.auth.models import TokenPair
from api.logic.logic import Logic
from api.storage.models import User
from fastapi import HTTPException, Request, Response, WebSocket


class RouterAuthUtils:

    @staticmethod
    def assert_logged_out(request: Request) -> None:
        """
        Check if the user is logged out by verifying the presence of access and refresh tokens.
        This method checks if both tokens are missing from the response cookies.
        Args:
            response (Response): The response object to check for tokens.
        Returns:
            bool: True if the user is logged out (both tokens are missing), False otherwise.
        """
        if request.cookies.get("access_token") and request.cookies.get("refresh_token"):
            raise HTTPException(
                status_code=401,
                detail="User is already logged in",
            )
        
    @staticmethod
    def assert_not_logged_out(request: Request) -> None:
        """
        Check if the user is logged in by verifying the presence of access and refresh tokens.
        This method checks if both tokens are present in the request cookies.
        Args:
            response (Response): The response object to check for tokens.
        Returns:
            bool: True if the user is logged out (both tokens are missing), False otherwise.
        """
        if not request.cookies.get("access_token") and not request.cookies.get("refresh_token"):
            raise HTTPException(
                status_code=200,
                detail="User is already logged out",
            )

    @staticmethod
    def clear_tokens(response: Response) -> None:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

    @staticmethod
    def update_tokens(tokens: TokenPair, response: Response) -> None:
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
            value=tokens.access_token,
            httponly=True,  # Prevent JavaScript access
            secure=True,    # Use HTTPS in production
            samesite="strict",  # CSRF protection
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Token expiration
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
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
    
    @staticmethod
    async def get_current_user_ws(websocket: WebSocket) -> tuple[User, WebSocket]:
        token = websocket.cookies.get("access_token")
        user = Logic.get_current_user(token)
        return user, websocket
