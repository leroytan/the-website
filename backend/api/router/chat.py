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
        receiver_id = data_dict["receiver_id"]
        content = data_dict["content"]
        
        message = NewChatMessage(
            content=content,
            receiverId=receiver_id,
        )

        await ChatLogic.handle_message(active_connections, message, user.id)


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
    # print(request.cookies.get("access_token"))
    # user = await RouterAuthUtils.get_current_user(request)
    messages = ChatLogic.get_chat_history(id, user.id, last_message_id, message_count)
    message_count = len(messages)
    last_unretrieved_message_id = messages[message_count - 1].id - 1 if message_count > 0 else -1
    return {
        "messages": messages,
        "message_count": message_count,
        "last_unretrieved_message_id": last_unretrieved_message_id,
    }

@router.put("/api/chat/{id}/unlock")
async def unlock_chat(id: int, user: User = Depends(RouterAuthUtils.get_current_user)) -> None:
    """
    Unlock chat with a user.

    Args:
        id (int): The ID of the user to unlock chat with.
        user (User): The current user.
    """
    return ChatLogic.unlock_chat(id, user.id)

@router.put("/api/chat/{id}/messages/read")
async def mark_messages_as_read(id: int, message_ids: str, user: User = Depends(RouterAuthUtils.get_current_user)) -> None:
    """
    Mark chat messages as read.

    Args:
        id (int): The ID of the chat to mark messages as read.
        message_ids: List of message IDs to mark as read.
        user (User): The current user.
    """
    # Convert the message_ids string to a list of integers
    message_ids = json.loads(message_ids)
    # Ensure that message_ids is a list of integers
    if not isinstance(message_ids, list) or not all(isinstance(i, int) for i in message_ids):
        raise ValueError("message_ids must be a list of integers.")
    
    # Call the logic function to mark messages as read
    ChatLogic.mark_messages_as_read(id, message_ids, user.id)

    return {"message": "Messages marked as read."}

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