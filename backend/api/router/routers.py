from api.router.assignment import router as assignment_router
from api.router.auth import router as auth_router
from api.router.tutor import router as tutor_router

# export
routers = [
    auth_router,
    tutor_router,
    assignment_router
]