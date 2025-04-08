from api.logic.filter_logic import FilterLogic
from api.router.models import Assignment as AssignmentView
from api.router.models import AssignmentSlot as AssignmentSlotView
from api.router.models import SearchQuery
from api.storage.models import Assignment, Level, Subject
from api.storage.storage_service import StorageService
from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session


class AssignmentLogic:

    @staticmethod
    def convert_assignment_to_view(session: Session, assignment: Assignment):

        session.add(assignment)

        # Extract subject and level names
        subject_names = [subject.name for subject in assignment.subjects] if assignment.subjects else []
        level_names = [level.name for level in assignment.levels] if assignment.levels else []
        slots = [
            AssignmentSlotView(
                id=slot.id,
                day=slot.day,
                startTime=slot.startTime,
                endTime=slot.endTime,
            )
            for slot in assignment.availableSlots
        ]
        return AssignmentView(
            id=assignment.id,
            datetime=assignment.datetime,
            title=assignment.title,
            requesterId=assignment.requesterId,
            tutorId=assignment.tutorId,
            estimatedRate=assignment.estimatedRate,
            weeklyFrequency=assignment.weeklyFrequency,
            availableSlots=slots,
            specialRequests=assignment.specialRequests,
            subjects=subject_names,
            levels=level_names,
            status=assignment.status
        )
        

    @staticmethod
    def search_assignments(search_query: SearchQuery) -> list[AssignmentView]:

        filters = []

        # General search (matching name, location, or aboutMe)
        if search_query.query:
            general_query = f"%{search_query.query}%"  # SQL LIKE pattern
            filters.append(or_(
                Assignment.title.ilike(general_query),
                Assignment.specialRequests.ilike(general_query),
            ))

        # get filters from the search query
        parsed_filters = FilterLogic.parse_filters(search_query.filters)

        # Filter by subjects
        if "subject" in parsed_filters:
            filters.append(Assignment.subjects.any(Subject.id.in_(parsed_filters["subject"])))

        # Filter by levels
        if "level" in parsed_filters:
            filters.append(Assignment.levels.any(Level.id.in_(parsed_filters["level"])))

        with Session(StorageService.engine) as session:

            assignments = StorageService.find(session, filters, Assignment)
            # raise HTTPException(
            #     status_code=401,
            #     detail=str(assignments)
            # )
            # Convert the list of Tutor objects to TutorPublicSummary objects            
            return [AssignmentLogic.convert_assignment_to_view(session, assgn) for assgn in assignments]