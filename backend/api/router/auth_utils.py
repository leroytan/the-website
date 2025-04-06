from api.logic.logic import Logic
from api.storage.models import User
from fastapi import Request, Response


class AuthUtils:

    @staticmethod
    def clear_tokens(response: Response) -> None:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

    @staticmethod
    async def get_current_user(request: Request) -> User:
        token = request.cookies.get("access_token")
        user = Logic.get_current_user(token)
        return user
