from api.router.assignment import router as assignment_router
from api.router.auth import router as auth_router
from api.router.chat import router as chat_router
from api.router.course import router as course_router
from api.router.me import router as me_router
from api.router.payment import router as payment_router
from api.router.reviews import router as reviews_router
from api.router.tutor import router as tutor_router
from api.router.user import router as user_router

# export
routers = [
    auth_router,
    user_router,
    chat_router,
    course_router,
    assignment_router,
    payment_router,
    reviews_router,
    tutor_router,
    me_router,
]