import json

from api.logic.chat_logic import ChatLogic
from api.router.auth_utils import RouterAuthUtils
from api.router.models import NewChatMessage
from api.storage.models import User
from fastapi import Depends, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

router = APIRouter()

active_connections = {}

@router.websocket("/ws/chat")
async def websocket_endpoint(pair: tuple[User, WebSocket] = Depends(RouterAuthUtils.get_current_user_ws)):
    user, websocket = pair
    await websocket.accept()
    active_connections[user.id] = websocket
    while True:
        data = await websocket.receive_text()
        data_dict = json.loads(data)
        chat_id = data_dict["chat_id"]
        content = data_dict["content"]
        
        message = NewChatMessage(
            content=content,
            chat_id=chat_id,
        )

        await ChatLogic.handle_private_message(active_connections, message, user.id)

@router.post("/api/chat/new")
async def create_chat(request: Request, user: User = Depends(RouterAuthUtils.get_current_user)) -> dict:
    """
    Create a new chat between two users.

    Args:
        request (Request): The request object containing the chat details.
        user (User): The current user.
    Returns:
        dict: A dictionary containing the chat ID and other relevant information.
    """
    data = await request.json()
    # TODO: can potentially use obfuscated user ID
    # to prevent user from having to know the ID of the other user
    other_id = data.get("other_id")
    chat = ChatLogic.get_or_create_private_chat(user.id, other_id)

    return chat


@router.get("/api/chat/{id}")
async def get_chat_messages(id: int, user: User = Depends(RouterAuthUtils.get_current_user), last_message_id: int = -1, message_count: int = 50) -> list[dict]:
    """
    Get chat messages between two users.

    Args:
        id (int): The ID of the user to get chat history with.
        last_message_id (int): The ID of the last message received.
        message_count (int): The number of messages to retrieve prior to (and including) the last message.
        user (User): The current user.
    Returns:
        list[ChatMessage]: List of chat messages.
    """
    messages = ChatLogic.get_private_chat_history(id, user.id, last_message_id, message_count)
    message_count = len(messages)
    last_unretrieved_message_id = messages[message_count - 1].id - 1 if message_count > 0 else -1
    return {
        "messages": messages,
        "message_count": message_count,
        "last_unretrieved_message_id": last_unretrieved_message_id,
    }


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