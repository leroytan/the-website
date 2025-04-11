import json

from api.logic.chat_logic import ChatLogic
from api.router.auth_utils import RouterAuthUtils
from api.router.models import NewChatMessage
from api.storage.models import User
from api.storage.storage_service import StorageService
from fastapi import Depends, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

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