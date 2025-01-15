from fastapi import APIRouter, Request, Response

from api.logic.course_logic import CourseLogic

from api.router.models import CoursePublicSummary, CourseModule

router = APIRouter()

@router.get("/api/courses")
async def get_courses():
    # TODO: handle difference in logic when the user is logged in.
    return CourseLogic.get_public_summaries()

@router.get("/api/courses/:course-id/module")
async def get_course_modules() -> list[CourseModule]:  # TODO: figure out if it is possible to return a list of pydantic objects natively, else make a simple translator  
    # TODO: create static method in courselogic
    return []

@router.get("/api/courses/:course-id/module/:id")
async def get_course_module_content() -> CourseModule:  # TODO: figure out if it is possible to return pydantic objects natively, else make a simple translator  
    # TODO: create static method in courselogic
    pass
    

