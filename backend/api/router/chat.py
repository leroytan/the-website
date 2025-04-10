from api.router.auth_utils import RouterAuthUtils
from api.storage.models import User
from fastapi import Depends, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

router = APIRouter()

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    print(websocket.cookies.get("access_token"))
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Decode data
        # Process data
        # Send response
        await websocket.send_text(f"Message text was: {data}")