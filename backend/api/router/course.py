from fastapi import APIRouter

from api.logic.course_logic import CourseLogic
from api.router.models import CourseModule, CoursePublicSummary

router = APIRouter()


@router.get("/api/courses")
async def get_courses(
    query: str = None,
) -> list[CoursePublicSummary]:
    # TODO: handle difference in logic when the user is logged in.
    # TODO: implement search functionality
    return CourseLogic.get_public_summaries()


@router.get("/api/courses/{course_id}/about")
async def get_course_about(course_id: str = None) -> str | None:
    # TODO: create static method in courselogic
    return None


@router.get("/api/courses/{course_id}/module")
async def get_course_modules(
    course_id: str = None,
) -> list[CourseModule]:
    # TODO: create static method in courselogic
    return []


@router.get("/api/courses/{course_id}/module/{id}")
async def get_course_module_content(
    course_id: str = None, id: int = None
) -> CourseModule | None:
    # TODO: create static method in courselogic
    return None
