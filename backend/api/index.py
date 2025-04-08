from api.router.routers import routers
from api.storage.models import Subject
from api.storage.storage_service import StorageService
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

StorageService.init_db()

### Create FastAPI instance with custom docs and openapi url
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

@app.get('/api/test')
async def test():
    query = {"id": "1"}
    update = {"name": "Algebra"}
    with Session(StorageService.engine) as session:
        return StorageService.update(session, query, update, Subject)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)