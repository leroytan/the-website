import enum
from collections.abc import Callable

from api.logic.filter_logic import FilterLogic
from api.router.models import AssignmentOwnerView, AssignmentPublicView
from api.router.models import AssignmentRequest as AssignmentRequestView
from api.router.models import AssignmentSlot as AssignmentSlotView
from api.router.models import NewAssignment, SearchQuery
from api.storage.models import (Assignment, AssignmentRequest,
                                AssignmentRequestStatus, AssignmentSlot,
                                AssignmentStatus, Level, Subject, Tutor, User)
from api.storage.storage_service import StorageService
from fastapi import HTTPException
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, aliased


class ViewType(enum.Enum):
    OWNER = "owner"
    PUBLIC = "public"

class AssignmentLogic:

    @staticmethod
    def convert_assignment_to_view(session: Session, assignment: Assignment, view_type: ViewType = ViewType.PUBLIC, user_id: int = None) -> AssignmentOwnerView | AssignmentPublicView:
        session.add(assignment)
        
        # Common conversion logic
        base_data = {
            "id": assignment.id,
            "created_at": assignment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": assignment.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "title": assignment.title,
            "owner_id": assignment.owner_id,
            "estimated_rate": assignment.estimated_rate,
            "weekly_frequency": assignment.weekly_frequency,
            "available_slots": [
                AssignmentSlotView(
                    id=slot.id,
                    day=slot.day,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                )
                for slot in assignment.available_slots
            ],
            "special_requests": assignment.special_requests,
            "subjects": [subject.name for subject in assignment.subjects] if assignment.subjects else [],
            "levels": [level.name for level in assignment.levels] if assignment.levels else [],
            "status": assignment.status,
            "location": assignment.location,
        }
        
        if view_type == ViewType.OWNER:
            base_data["tutor_id"] = assignment.tutor_id
            base_data["requests"] = [
                AssignmentRequestView(
                    id=request.id,
                    created_at=request.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=request.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    tutor_id=request.tutor_id,
                    status=request.status
                )
                for request in assignment.assignment_requests
            ]
            return AssignmentOwnerView(**base_data)
        else:
            if user_id is not None:
                for request in assignment.assignment_requests:
                    if request.tutor_id == user_id:
                        base_data["applied"] = True
                        break
            return AssignmentPublicView(**base_data)
        

    @staticmethod
    def search_assignments(search_query: SearchQuery, user_id: int = None) -> list[AssignmentPublicView]:

        with Session(StorageService.engine) as session:
            filters = []

            tutor_alias = aliased(Tutor)
            user_alias = aliased(User)
            owner_alias = aliased(User)
            # Join the Assignment table with the Tutor and User tables
            statement = session.query(Assignment)
            statement = statement.outerjoin(tutor_alias, Assignment.tutor)
            statement = statement.outerjoin(user_alias, tutor_alias.user)
            statement = statement.outerjoin(owner_alias, Assignment.owner)

            # General search (matching name, location, or about_me)
            if search_query.query:
                general_query = f"%{search_query.query}%"  # SQL LIKE pattern
                filters.append(or_(
                    Assignment.title.ilike(general_query),
                    Assignment.special_requests.ilike(general_query),
                    user_alias.name.ilike(general_query),
                    owner_alias.name.ilike(general_query),
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
            summaries = [AssignmentLogic.convert_assignment_to_view(session, assignment, ViewType.PUBLIC, user_id) for assignment in assignments]

            return summaries
        
    @staticmethod
    def new_assignment(new_assignment: NewAssignment, user_id: str|int) -> AssignmentOwnerView:
        with Session(StorageService.engine) as session:

            # Create a new assignment
            assignment = Assignment(
                title=new_assignment.title,
                owner_id=user_id,
                estimated_rate=new_assignment.estimated_rate,
                weekly_frequency=new_assignment.weekly_frequency,
                special_requests=new_assignment.special_requests,
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
            for slot in new_assignment.available_slots:
                assignment_slot = AssignmentSlot(
                    day=slot.day,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    assignment_id=assignment.id
                )
                session.add(assignment_slot)
            assignment.available_slots = session.query(AssignmentSlot).filter(AssignmentSlot.assignment_id == assignment.id).all()

            session.commit()
            session.refresh(assignment)
            return AssignmentLogic.convert_assignment_to_view(session, assignment, ViewType.OWNER)
        
    @staticmethod
    def get_assignment_by_id(id: str | int, user_id: int = None) -> AssignmentOwnerView | AssignmentPublicView:
        with Session(StorageService.engine) as session:
            assignment = StorageService.find(session, {"id": id}, Assignment, find_one=True)
            if not assignment:
                raise HTTPException(
                    status_code=404,
                    detail="Assignment not found"
                )
            view_type = ViewType.OWNER if assignment.owner_id == user_id else ViewType.PUBLIC
            return AssignmentLogic.convert_assignment_to_view(session, assignment, view_type, user_id)
        
    @staticmethod
    def update_assignment_by_id(id: str | int, assignment_update: NewAssignment, assert_user_authorized: Callable[[int], None]) -> AssignmentOwnerView:
        with Session(StorageService.engine) as session:
            # Update the assignment
            assignment_dict = assignment_update.model_dump()

            assignment_dict.pop("available_slots", None)
            assignment_dict.pop("subjects", None)
            assignment_dict.pop("levels", None)

            assignment = StorageService.update(session, {"id": id}, assignment_dict, Assignment)
            if not assignment:
                raise HTTPException(
                    status_code=404,
                    detail="Assignment not found"
                )
            
            # Check if the user is the owner of the assignment
            assert_user_authorized(assignment.owner_id)

            session.add(assignment)
            # Update subjects and levels
            assignment.subjects = session.query(Subject).filter(Subject.name.in_(assignment_update.subjects)).all()
            assignment.levels = session.query(Level).filter(Level.name.in_(assignment_update.levels)).all()

            # Clear slots
            StorageService.delete(session, {"assignment_id": assignment.id}, AssignmentSlot)
            # Update available slots
            for slot in assignment_update.available_slots:
                assignment_slot = StorageService.insert(session, AssignmentSlot(
                    day=slot.day,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    assignment_id=assignment.id
                ))
                session.add(assignment_slot)
            assignment.available_slots = session.query(AssignmentSlot).filter(AssignmentSlot.assignment_id == assignment.id).all()

            session.commit()
            session.refresh(assignment)
            return AssignmentLogic.convert_assignment_to_view(session, assignment, ViewType.OWNER)
        
    @staticmethod
    def request_assignment(assignment_id: str | int, tutor_id: str | int) -> None:
        with Session(StorageService.engine) as session:
            # Find the assignment
            assignment = StorageService.find(session, {"id": assignment_id}, Assignment, find_one=True)
            if not assignment:
                raise HTTPException(
                    status_code=404,
                    detail="Assignment not found"
                )

            # Check if the assignment is open
            if assignment.status != AssignmentStatus.OPEN or assignment.tutor_id is not None:
                raise HTTPException(
                    status_code=400,
                    detail="Assignment is not open for requests"
                )
            if assignment.owner_id == tutor_id:
                raise HTTPException(
                    status_code=400,
                    detail="Tutor cannot request their own assignment"
                )
            
            # Create a request
            try:
                StorageService.insert(session, AssignmentRequest(
                    assignment_id=assignment.id,
                    tutor_id=tutor_id
                ))
            except IntegrityError as e:
                if isinstance(e.orig, ForeignKeyViolation):
                    raise HTTPException(
                        status_code=409,
                        detail=f"Tutor with this id={tutor_id} does not exist"
                    )
                elif isinstance(e.orig, UniqueViolation):  # Should not happen
                    raise HTTPException(
                        status_code=409,
                        detail="Assignment request already exists"
                    )
                else:
                    raise e
    

    @staticmethod
    def change_assignment_request_status(assignment_request_id: str | int, status: str, assert_user_authorized: Callable[[int], None]) -> None:
        with Session(StorageService.engine) as session:
            # Find the assignment request
            assignment_request = StorageService.find(session, {"id": assignment_request_id}, AssignmentRequest, find_one=True)
            if not assignment_request:
                raise HTTPException(
                    status_code=404,
                    detail="Assignment request not found"
                )

            session.add(assignment_request)

            # TODO: Determine if owner should be allowed to reopen request once it is rejected or accepted
            # if assignment_request.status != AssignmentRequestStatus.PENDING:
            #     raise HTTPException(
            #         status_code=409,
            #         detail="Assignment request is not pending. Cannot change status."
            #     )

            # Check if the user is the owner of the assignment
            assert_user_authorized(assignment_request.assignment.owner_id)

            # Update the assignment with the tutor_id
            assignment = StorageService.update(session, {"id": assignment_request.assignment_id},
                                               {"tutor_id": assignment_request.tutor_id, "status": AssignmentStatus.FILLED},
                                                 Assignment)
            if not assignment:
                raise HTTPException(
                    status_code=404,
                    detail="Assignment not found"
                )
            
            # Directly access the enum member using getattr
            assignment_request.status = getattr(AssignmentRequestStatus, status, None)

            # Optionally handle invalid status
            if assignment_request.status is None:
                raise ValueError(f"Invalid status: {status}")

            session.commit()
