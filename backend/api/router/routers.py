from api.router import (
    assignment,
    auth,
    chat,
    course,
    me,
    payment,
    reviews,
    tutor,
    user,
    websocket,
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
    websocket.router,
]
