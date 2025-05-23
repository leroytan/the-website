from api.config import settings
from api.router.auth_utils import RouterAuthUtils
from api.router.routers import routers
from api.storage.models import User
from api.storage.storage_service import StorageService
from fastapi import Depends, FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

StorageService.init_db()

app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

for router in routers:
    app.include_router(router)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"message": "Error: The requested route or method does not exist."}
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

@app.head("/")
async def root_head():
    return {"message": "Your server is running."}

@app.get('/api/ping')
async def ping_get():
    return {"message": "pong"}

@app.post('/api/ping')
async def ping_post():
    return {"message": "pong"}

@app.head('/api/ping')
async def ping_head():
    return {"message": "pong"}

@app.websocket("/ws/ping")
async def websocket_ping(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        if data == "ping":
            await websocket.send_text("pong")
        else:
            await websocket.send_text("Invalid message. Send 'ping' to receive 'pong'.")

# Simple echo websocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"Received message: {data}")
        await websocket.send_text(f"Message text was: {data}")

@app.websocket("/ws/protected")
async def websocket_endpoint(pair: tuple[User, WebSocket] = Depends(RouterAuthUtils.get_current_user_ws)):
    user, websocket = pair
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"Received message from [id: {user.id}] {user.name}: {data}")
        await websocket.send_text(f"Message text was: {data}")

origins = settings.allowed_origins.split(",")
print(f"Allowed origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)