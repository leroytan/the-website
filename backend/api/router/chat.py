import asyncio
import json

from api.logic.chat_logic import ChatLogic
from api.router.auth_utils import RouterAuthUtils
from fastapi import Depends
from api.storage.models import User
from api.router.models import ChatCreationInfo, NewChatMessage, ChatPreview
from api.storage.models import User, ChatMessageType
from fastapi import Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

router = APIRouter()

# No longer needed as they are static members of ChatLogic
# mutex = asyncio.Lock()
# active_connections = {}

# Route for getting jwt for websocket purposes
@router.get("/api/chat/jwt")
async def get_jwt(request: Request, user: User = Depends(RouterAuthUtils.get_current_user)) -> dict:
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

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, access_token: str = ""):
    user = RouterAuthUtils.get_user_from_jwt(access_token)
    await websocket.accept()
    async with ChatLogic.mutex:
        ChatLogic.active_connections[user.id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            data_dict = json.loads(data)
            chat_id = data_dict["chat_id"]
            content = data_dict["content"]
            message_type = data_dict.get("message_type", ChatMessageType.TEXT_MESSAGE)
            
            message = NewChatMessage(
                content=content,
                chat_id=chat_id,
                message_type=message_type
            )
 
            await ChatLogic.handle_private_message(message, user.id)
    except WebSocketDisconnect:
        async with ChatLogic.mutex:
            if user.id in ChatLogic.active_connections:
                del ChatLogic.active_connections[user.id]
        print(f"WebSocket connection closed for user {user.id}")

@router.post("/api/chat/get-or-create")
async def get_or_create_chat(chat_info: ChatCreationInfo, user: User = Depends(RouterAuthUtils.get_current_user)) -> ChatPreview:
    """
    Create a new chat between two users.

    Args:
        request (Request): The request object containing the chat details.
        user (User): The current user.
    Returns:
        dict: A dictionary containing the chat ID and other relevant information.
    """
    return ChatLogic.get_or_create_private_chat(user.id, chat_info.other_user_id)


@router.get("/api/chat/{id}")
async def get_chat_messages(id: int, user: User = Depends(RouterAuthUtils.get_current_user), created_before: str = None, limit: int = 50) -> dict:
    return ChatLogic.get_private_chat_history(id, user.id, created_before, limit)

# route for updating state of chat as read
@router.post("/api/chat/{id}/read")
async def mark_chat_as_read(id: int, user: User = Depends(RouterAuthUtils.get_current_user)) -> dict:
    """
    Mark a chat as read for the current user.

    Args:
        id (int): The ID of the chat to mark as read.
        user (User): The current user.
    Returns:
        dict: A dictionary indicating success or failure.
    """
    ChatLogic.mark_chat_as_read(id, user.id)
    return {"status": "success", "message": "Chat marked as read."}

@router.get("/api/chats")
async def get_chats(user: User = Depends(RouterAuthUtils.get_current_user)) -> dict:
    """
    Get all chats for the current user.

    Args:
        user (User): The current user.
    Returns:
        dict: A dictionary containing the list of chats.
    """
    return ChatLogic.get_private_chats(user.id)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/chat");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@router.get("/")
async def get():
    return HTMLResponse(html)