from api.logic.filter_logic import FilterLogic
from api.router.models import Assignment as AssignmentView
from api.router.models import AssignmentSlot as AssignmentSlotView
from api.router.models import NewAssignment, SearchQuery
from api.storage.models import (Assignment, AssignmentSlot, AssignmentStatus,
                                Level, Subject, Tutor, User)
from api.storage.storage_service import StorageService
from fastapi import HTTPException
from psycopg2.errors import ForeignKeyViolation
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, aliased


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
            datetime=assignment.datetime.strftime("%Y-%m-%d %H:%M:%S"),
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

        with Session(StorageService.engine) as session:
            filters = []

            tutor_alias = aliased(Tutor)
            user_alias = aliased(User)
            requester_alias = aliased(User)
            # Join the Assignment table with the Tutor and User tables
            statement = session.query(Assignment)
            statement = statement.outerjoin(tutor_alias, Assignment.tutor)
            statement = statement.outerjoin(user_alias, tutor_alias.user)
            statement = statement.outerjoin(requester_alias, Assignment.requester)

            # General search (matching name, location, or aboutMe)
            if search_query.query:
                general_query = f"%{search_query.query}%"  # SQL LIKE pattern
                filters.append(or_(
                    Assignment.title.ilike(general_query),
                    Assignment.specialRequests.ilike(general_query),
                    user_alias.name.ilike(general_query),
                    requester_alias.name.ilike(general_query),
                ))

            # get filters from the search query
            parsed_filters = FilterLogic.parse_filters(search_query.filters)

            # Filter by subjects
            if "subject" in parsed_filters:
                filters.append(Assignment.subjects.any(Subject.id.in_(parsed_filters["subject"])))

            # Filter by levels
            if "level" in parsed_filters:
                filters.append(Assignment.levels.any(Level.id.in_(parsed_filters["level"])))

            statement = statement.filter(and_(*filters))

            assignments = StorageService.find(session, statement, Assignment)

            # Convert the list of Tutor objects to TutorPublicSummary objects            
            summaries = [AssignmentLogic.convert_assignment_to_view(session, assignment) for assignment in assignments]

            return summaries
        
    @staticmethod
    def create_assignment(new_assignment: NewAssignment, user_id: str|int) -> AssignmentView:
        with Session(StorageService.engine) as session:

            # Create a new assignment
            assignment = Assignment(
                title=new_assignment.title,
                requesterId=user_id,
                estimatedRate=new_assignment.estimatedRate,
                weeklyFrequency=new_assignment.weeklyFrequency,
                specialRequests=new_assignment.specialRequests,
                status=AssignmentStatus.OPEN
            )

            try:
                assignment = StorageService.insert(session, assignment)
            except IntegrityError as e:
                if isinstance(e.orig, ForeignKeyViolation):
                    raise HTTPException(
                        status_code=409,
                        detail=f"Requester with this id={user_id} does not exist"
                    )
                else:
                    raise HTTPException(
                        status_code=500,
                        detail="Internal server error"
                    )

            session.add(assignment)

            assignment.subjects = session.query(Subject).filter(Subject.name.in_(new_assignment.subjects)).all()
            assignment.levels = session.query(Level).filter(Level.name.in_(new_assignment.levels)).all()
        
            # Create assignment slots
            for slot in new_assignment.availableSlots:
                assignment_slot = AssignmentSlot(
                    day=slot.day,
                    startTime=slot.startTime,
                    endTime=slot.endTime,
                    assignmentId=assignment.id
                )
                session.add(assignment_slot)
            assignment.availableSlots = session.query(AssignmentSlot).filter(AssignmentSlot.assignmentId == assignment.id).all()

            session.commit()
            session.refresh(assignment)
            return AssignmentLogic.convert_assignment_to_view(session, assignment)