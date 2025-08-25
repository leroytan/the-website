import asyncio
import json
from typing import Dict, List

from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect

from api.router.auth_utils import RouterAuthUtils
from api.storage.models import User

router = APIRouter()


class WebSocketManager:
    mutex = asyncio.Lock()
    active_connections: Dict[int, List[WebSocket]] = {}

    @classmethod
    async def connect(cls, websocket: WebSocket, user_id: int):
        await websocket.accept()
        async with cls.mutex:
            if user_id not in cls.active_connections:
                cls.active_connections[user_id] = []
            cls.active_connections[user_id].append(websocket)

    @classmethod
    async def disconnect(cls, websocket: WebSocket, user_id: int):
        async with cls.mutex:
            if user_id in cls.active_connections:
                cls.active_connections[user_id].remove(websocket)
                if not cls.active_connections[user_id]:
                    del cls.active_connections[user_id]

    @classmethod
    async def send_personal_notification(cls, user_id: int, message: str):
        async with cls.mutex:
            if user_id in cls.active_connections:
                for connection in cls.active_connections[user_id]:
                    await connection.send_text(message)

    @classmethod
    async def broadcast_notification(cls, message: str):
        async with cls.mutex:
            for user_connections in cls.active_connections.values():
                for connection in user_connections:
                    await connection.send_text(message)


# Route for getting jwt for websocket purposes
@router.get("/api/ws/jwt")
async def get_jwt(
    request: Request, user: User = Depends(RouterAuthUtils.get_current_user)
) -> dict[str, str]:
    """
    Get JWT for websocket authentication.

    Args:
        user (User): The current user.
    Returns:
        dict: A dictionary containing the JWT token.
    """
    return {
        "access_token": RouterAuthUtils.get_jwt(request),
    }


@router.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket, access_token: str = ""):
    user = RouterAuthUtils.get_user_from_jwt(access_token)
    await WebSocketManager.connect(websocket, user.id)

    try:
        while True:
            # Keep the connection open and listen for any incoming messages
            data = await websocket.receive_text()
            # Optional: Add custom message handling logic here
            try:
                parsed_data = json.loads(data)
                # Handle specific message types if needed
            except json.JSONDecodeError:
                # Handle non-JSON messages or log an error
                pass
    except WebSocketDisconnect:
        await WebSocketManager.disconnect(websocket, user.id)
        print(f"WebSocket connection closed for user {user.id}")
