from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the routers
from api.router.auth import router as auth_router
from api.router.tutor import router as tutor_router
from api.storage.storage_service import StorageService

StorageService.init_db()

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

app.include_router(tutor_router)
app.include_router(auth_router)

@app.get("/api/helloFastApi")
def hello_fast_api():
    d = {
        "message": "Hello from FastAPI"
    }
    return d

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)