from api.auth.models import TokenPair
from api.config import settings
from api.logic.logic import Logic
from api.storage.models import User
from fastapi import HTTPException, Request, WebSocket, Response
from typing import Optional

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = settings.refresh_token_expire_minutes

class RouterAuthUtils:

    @staticmethod
    def assert_logged_out(request: Request) -> None:
        """
        Check if the user is logged out by verifying the presence of access and refresh tokens.
        This method checks if the user is logged out by attempting to retrieve the current user
        Args:
            reqest (Request): The request object to check for tokens.
        Returns:
            bool: True if the user is logged out (both tokens are missing), False otherwise.
        """
        try:
            _ = RouterAuthUtils.get_current_user(request)
        except HTTPException as e:
            # if get_current_user raises an exception, it means the user is logged out
            # and we can proceed with the login/signup process
            if e.status_code == 401:
                return
            # if the exception is not due to missing tokens, re-raise it
            # could be internal server error or other issues
            raise e
        # if we reach this point, it means the user is logged in
            
        # if get_current_user does not raise an exception, it means the user is logged in
        # and we should not allow login/signup
        raise HTTPException(
            status_code=403,
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
    def _get_cookie_params(origin: str) -> dict:
        """Helper method to get consistent cookie parameters"""
        if origin.startswith("http://"):
            domain = None
        elif origin.startswith("https://"):
            domain = origin[8:]
        else:
            domain = origin
        
        return {
            "domain": domain,
            "httponly": True,
            "secure": True,
            "samesite": "strict"
        }

    @staticmethod
    def clear_tokens(response: Response, origin: str) -> None:
        """
        Clear access and refresh tokens from cookies.
        Args:
            response (Response): The response object to clear cookies from.
            origin (str): The origin URL to determine cookie domain (must match set_cookie).
        """
        cookie_params = RouterAuthUtils._get_cookie_params(origin)
        
        response.delete_cookie(
            key="access_token",
            **cookie_params
        )
        response.delete_cookie(
            key="refresh_token",
            **cookie_params
        )

    @staticmethod
    def update_tokens(tokens: TokenPair, response: Response, origin: str) -> None:
        """
        Update the response with new access and refresh tokens.
        This method sets the tokens as HTTP-only cookies in the response,
        which helps prevent JavaScript access and enhances security.
        Args:
            tokens (TokenPair): A TokenPair containing the new access and refresh tokens.
            response (Response): The response object to update with the new tokens.
            origin (str): The origin URL to determine cookie domain.
        """
        cookie_params = RouterAuthUtils._get_cookie_params(origin)
        
        response.set_cookie(
            key="access_token",
            value=tokens.access_token,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            **cookie_params
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
            **cookie_params
        )


    @staticmethod
    def get_jwt(request: Request) -> str:
        """
        Generate a JWT token for the user.
        This method creates a JWT token that can be used for authentication
        in WebSocket connections.
        Args:
            request (Request): The request object containing the user's information.
        Returns:
            str: The retrieved JWT token.
        """
        return request.cookies.get("access_token")

    @staticmethod
    def get_current_user(request: Request) -> User:
        access_token = RouterAuthUtils.get_jwt(request)
        return RouterAuthUtils.get_user_from_jwt(access_token)
    
    @staticmethod
    def get_user_from_jwt(token: str) -> User:
        """
        Get the user from the JWT token.
        This method extracts the user information from the JWT token.
        Args:
            token (str): The JWT token.
        Returns:
            User: The user object extracted from the token.
        """
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        return Logic.get_current_user(token, credentials_exception)
    
    @staticmethod
    def get_current_user_ws(websocket: WebSocket) -> tuple[User, WebSocket]:
        token = websocket.cookies.get("access_token")
        user = Logic.get_current_user(token)
        return user, websocket
