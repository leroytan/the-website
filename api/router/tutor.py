from fastapi import APIRouter, Request, Response

from api.logic.tutor_logic import TutorLogic

from api.router.models import TutorSearchQuery

router = APIRouter()

@router.get("/api/tutors")
async def get_tutors():
    tutors = TutorLogic.get_public_summaries()
    return tutors

@router.post("/api/tutors/search")
async def search_tutors(request: Request, response: Response):
    """
    Handles the searching of specific tutors using fields

    Args:
        request (Request): The request object containing the login data
        response (Response): The response object used to indicate if the search
                            was successful.

    Returns:
        str: A success message confirming the search process.

    Raises: (TBC)
        HTTPException: IfIf the login credentials are invalid or the login process 
                        fails, an HTTP error is raised with an appropriate status code.
    """

    data = await request.json()

    search_query = TutorSearchQuery(
        query=data["query"],
        subjects=data["subjects"],
        levels=data["levels"],
    )

    results = TutorLogic.search_tutors(search_query)

    return results

@router.get("/api/tutors/profile/:id")  # TODO: figure out how to handle dynamic routes in fastapi
async def tutor_public_profile(request: Request, response: Response):
    return TutorLogic.find_tutor_by_id(":id") 