from fastapi import APIRouter
from api.router import (
    auth, 
    user, 
    course, 
    assignment, 
    chat, 
    tutor, 
    reviews, 
    me, 
    payment,
)

# Change from router to a list of routers
routers = [
    auth.router,
    user.router,
    course.router,
    assignment.router,
    chat.router,
    tutor.router,
    reviews.router,
    me.router,
    payment.router,
]