import asyncio
import enum
import json
import math
from collections.abc import Callable

from api.logic.chat_logic import ChatLogic
from api.logic.filter_logic import FilterLogic
from api.logic.sort_logic import SortLogic
from api.logic.user_logic import UserLogic
from api.router.models import (AssignmentOwnerView, AssignmentPublicView,
                               AssignmentRequestView, AssignmentSlotView,
                               NewAssignment, NewAssignmentRequest,
                               SearchQuery, NewChatMessage, ModifiedAssignmentRequest)
from api.storage.models import (Assignment, AssignmentRequest,
                                AssignmentRequestStatus, AssignmentSlot,
                                AssignmentStatus, Level, Subject, Tutor, User)
from api.storage.storage_service import StorageService
from fastapi import HTTPException
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, aliased, joinedload


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
            "created_at": assignment.created_at.isoformat(),
            "updated_at": assignment.updated_at.isoformat(),
            "title": assignment.title,
            "owner_id": assignment.owner_id,
            "estimated_rate_hourly": assignment.estimated_rate_hourly,
            "lesson_duration": assignment.lesson_duration,
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
            "level": assignment.level.name,
            "status": assignment.status,
            "location": assignment.location,
        }
        
        if view_type == ViewType.OWNER:
            base_data["tutor_id"] = assignment.tutor_id
            base_data["requests"] = [
                AssignmentRequestView(
                    id=request.id,
                    created_at=request.created_at.isoformat(),
                    updated_at=request.updated_at.isoformat(),
                    tutor_id=request.tutor_id,
                    tutor_name=request.tutor.user.name,
                    tutor_profile_photo_url=UserLogic.get_profile_photo_url(request.tutor_id),
                    requested_rate_hourly=request.requested_rate_hourly,
                    requested_duration=request.requested_duration,
                    available_slots=[
                        AssignmentSlotView(
                            id=slot.id,
                            day=slot.day,
                            start_time=slot.start_time,
                            end_time=slot.end_time,
                        )
                        for slot in request.available_slots
                    ],
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
                        base_data["request_status"] = request.status.value
                        break
            return AssignmentPublicView(**base_data)
        

    @staticmethod
    def search_assignments(search_query: SearchQuery, user_id: int = None) -> dict:

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
            statement = statement.outerjoin(Assignment.level)

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
            parsed_filters = FilterLogic.parse_filters(search_query.filter_by)

            # Filter by subjects
            if "subject" in parsed_filters:
                filters.append(Assignment.subjects.any(Subject.id.in_(parsed_filters["subject"])))

            # Filter by level
            if "level" in parsed_filters:
                filters.append(Assignment.level_id.in_(parsed_filters["level"]))

            statement = statement.filter(and_(*filters))
            try:
                # Default ordering is by created_at descending, then by id ascending
                statement = statement.order_by(SortLogic.get_sorting(Assignment, search_query.sort_by))
            except ValueError as e:
                raise HTTPException(
                    status_code=400,
                    detail=str(e)
                )
                
            # Pagination
            page_size = search_query.page_size
            offset = (search_query.page_number - 1) * page_size
            num_pages = math.ceil(statement.count() / page_size)
            statement = statement.offset(offset).limit(page_size)
            assignments = statement.all()

            # Convert the list of Tutor objects to AssignmentPublicView objects            
            results = [AssignmentLogic.convert_assignment_to_view(session, assignment, ViewType.PUBLIC, user_id) for assignment in assignments]

            return {
                "results": results,
                "num_pages": num_pages,
            }
        
    @staticmethod
    def new_assignment(new_assignment: NewAssignment, user_id: int) -> AssignmentOwnerView:
        with Session(StorageService.engine) as session:

            level_id = session.query(Level).filter_by(name=new_assignment.level).one().id

            # Create a new assignment
            assignment = Assignment(
                title=new_assignment.title,
                owner_id=user_id,
                level_id=level_id,
                estimated_rate_hourly=new_assignment.estimated_rate_hourly,
                lesson_duration=new_assignment.lesson_duration,
                weekly_frequency=new_assignment.weekly_frequency,
                special_requests=new_assignment.special_requests,
                status=AssignmentStatus.OPEN,
                location=new_assignment.location,
            )

            try:
                session.add(assignment)

                assignment.subjects = session.query(Subject).filter(Subject.name.in_(new_assignment.subjects)).all()

                # Create assignment slots
                for slot in new_assignment.available_slots:
                    # TODO: Enforce that slot duration is >= lesson_duration
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
            except IntegrityError as e:
                if isinstance(e.orig, ForeignKeyViolation):
                    raise HTTPException(
                        status_code=409,
                        detail=f"Requester with this id={user_id} does not exist"
                    )
                else:
                    raise HTTPException(
                        status_code=500,
                        detail=e.orig.args[0]
                    )
                    
        
    @staticmethod
    def get_assignment_by_id(id: int, user_id: int = None) -> AssignmentOwnerView | AssignmentPublicView:
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

            level_id = session.query(Level).filter_by(name=assignment_update.level).one().id

            assignment_dict.pop("available_slots", None)
            assignment_dict.pop("subjects", None)
            assignment_dict.pop("level", None)
            assignment_dict["level_id"] = level_id

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
    def request_assignment(new_assignment_request: NewAssignmentRequest, tutor_id: str | int) -> None:
        with Session(StorageService.engine) as session:
            # Find the assignment
            assignment = session.query(Assignment).filter_by(id=new_assignment_request.assignment_id).first()
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
                assignment_req = AssignmentRequest(
                    assignment_id=assignment.id,
                    tutor_id=tutor_id,
                    requested_rate_hourly=new_assignment_request.requested_rate_hourly or assignment.estimated_rate_hourly,
                    requested_duration=new_assignment_request.requested_duration or assignment.lesson_duration,
                )

                session.add(assignment_req)
                session.flush()  # Ensure the assignment_req has an ID before adding slots

                # Create assignment slots
                for slot in new_assignment_request.available_slots:
                    assignment_slot = AssignmentSlot(
                        day=slot.day,
                        start_time=slot.start_time,
                        end_time=slot.end_time,
                        assignment_request_id=assignment_req.id
                    )
                    session.add(assignment_slot)
                session.commit()
            except IntegrityError as e:
                if isinstance(e.orig, ForeignKeyViolation):
                    raise HTTPException(
                        status_code=409,
                        detail=f"Tutor with this id={tutor_id} does not exist. You have not signed up to be a tutor."
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
            status = getattr(AssignmentRequestStatus, status, None)
            if status != AssignmentRequestStatus.REJECTED:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid status. Only 'REJECTED' is allowed."
                )

            # Find the assignment request
            assignment_request = session.query(AssignmentRequest).options(
                joinedload(AssignmentRequest.assignment)
            ).filter_by(id=assignment_request_id).first()
            if not assignment_request:
                raise HTTPException(
                    status_code=404,
                    detail="Assignment request not found"
                )

            # TODO: Determine if owner should be allowed to reopen request once it is rejected or accepted
            # if assignment_request.status != AssignmentRequestStatus.PENDING:
            #     raise HTTPException(
            #         status_code=409,
            #         detail="Assignment request is not pending. Cannot change status."
            #     )

            # Check if the user is the owner of the assignment
            assert_user_authorized(assignment_request.assignment.owner_id)

            # Update the assignment with the tutor_id
            assignment = assignment_request.assignment
            if not assignment:
                raise HTTPException(
                    status_code=404,
                    detail="Assignment not found"
                )
            if assignment.status != AssignmentStatus.OPEN:
                raise HTTPException(
                    status_code=400,
                    detail="Assignment is not open for requests"
                )
            if assignment.tutor_id is not None:
                raise HTTPException(
                    status_code=400,
                    detail="Assignment already has a tutor assigned"
                )
            
            if status == AssignmentRequestStatus.ACCEPTED:
                # If the status is ACCEPTED, we need to accept the assignment request
                AssignmentLogic.accept_assignment_request(assignment_request_id)
            
            # Update the assignment request status
            assignment_request.status = status

            # Optionally handle invalid status
            if assignment_request.status is None:
                raise ValueError(f"Invalid status: {status}")

            session.commit()

    @staticmethod    
    def get_created_assignments(user_id: int) -> list[AssignmentOwnerView]:
        # Get all assignments created by the user
        with Session(StorageService.engine) as session:
            assignments = StorageService.find(session, {"owner_id": user_id}, Assignment, find_one=False)
            if not assignments:
                return []
            
            # Convert to AssignmentOwnerView
            return [AssignmentLogic.convert_assignment_to_view(session, assignment, ViewType.OWNER) for assignment in assignments]
        
    @staticmethod
    def get_applied_assignments(user_id: int) -> list[AssignmentPublicView]:
        # Get all assignments applied by the user, and the associated request status for each.
        # An assignment is considered applied if the user is a tutor and has a request for that assignment.
        with Session(StorageService.engine) as session:
            assignments = session.query(Assignment).join(Assignment.assignment_requests).filter(
                AssignmentRequest.tutor_id == user_id
            ).all()
            if not assignments:
                return []
            
            # Convert to AssignmentPublicView
            return [AssignmentLogic.convert_assignment_to_view(session, assignment, ViewType.PUBLIC, user_id) for assignment in assignments]
        
    @staticmethod
    def accept_assignment_request(assignment_request_id: int) -> tuple[int, int]:
        with Session(StorageService.engine) as session:
            assignment_request = session.query(AssignmentRequest).filter_by(id=assignment_request_id).first()
            if not assignment_request:
                raise HTTPException( status_code=404, detail="Assignment request not found")
            elif assignment_request.status != AssignmentRequestStatus.PENDING:
                raise HTTPException( status_code=409, detail="Assignment request is not pending. Cannot accept.")
            
            assignment = assignment_request.assignment
            assignment.status = AssignmentStatus.FILLED
            assignment.tutor_id = assignment_request.tutor_id

            for request in assignment.assignment_requests:
                request.status = AssignmentRequestStatus.REJECTED

            assignment_request.status = AssignmentRequestStatus.ACCEPTED

            session.commit()

            return (assignment.owner_id, assignment_request.tutor_id)
        
    @staticmethod
    def get_assignment_owner_id(assignment_request_id: int) -> User:
        with Session(StorageService.engine) as session:
            assignment_request = session.query(AssignmentRequest).options(joinedload(AssignmentRequest.assignment)).filter_by(id=assignment_request_id).first()
            if not assignment_request:
                raise HTTPException(
                    status_code=404,
                    detail="Assignment request not found"
                )
            assignment = assignment_request.assignment
            if not assignment:
                raise HTTPException(
                    status_code=404,
                    detail="Assignment not found for the given request"
                )
            return assignment.owner_id
        
        
    @staticmethod
    def get_lesson_duration(assignment_request_id: int) -> int:
        with Session(StorageService.engine) as session:
            assignment_request = session.query(AssignmentRequest).options(joinedload(AssignmentRequest.assignment)).filter(
                AssignmentRequest.id == assignment_request_id
            ).first()
            if not assignment_request:
                raise HTTPException(
                    status_code=404,
                    detail="Assignment request not found"
                )
            if not assignment_request.assignment:
                raise HTTPException(
                    status_code=404,
                    detail="Assignment not found for the given request"
                )
            return assignment_request.assignment.lesson_duration
        
    @staticmethod
    def get_request_hourly_rate(assignment_request_id: int) -> int:
        with Session(StorageService.engine) as session:
            assignment_request = session.query(AssignmentRequest).filter_by(id=assignment_request_id).first()
            if not assignment_request:
                raise HTTPException(
                    status_code=404,
                    detail="Assignment request not found"
                )
            return assignment_request.requested_rate_hourly

    @staticmethod
    def get_assignment_request_by_id(assignment_request_id: int, assert_user_authorized: Callable[[int], None]) -> AssignmentRequestView:
        with Session(StorageService.engine) as session:
            assignment_request = session.query(AssignmentRequest).filter_by(
                id=assignment_request_id
            ).first()
            if not assignment_request:
                raise HTTPException(
                    status_code=404,
                    detail="Assignment request not found"
                )
            
            # Check if the user is the owner of the assignment
            assert_user_authorized(assignment_request.tutor_id)

            return AssignmentRequestView(
                id=assignment_request.id,
                created_at=assignment_request.created_at.isoformat(),
                updated_at=assignment_request.updated_at.isoformat(),
                tutor_id=assignment_request.tutor_id,
                tutor_name=assignment_request.tutor.user.name,
                tutor_profile_photo_url=UserLogic.get_profile_photo_url(assignment_request.tutor_id),
                requested_rate_hourly=assignment_request.requested_rate_hourly,
                requested_duration=assignment_request.requested_duration,
                available_slots=[
                    AssignmentSlotView(
                        id=slot.id,
                        day=slot.day,
                        start_time=slot.start_time,
                        end_time=slot.end_time,
                    )
                    for slot in assignment_request.available_slots
                ],
                status=str(assignment_request.status)
            )
        
    @staticmethod
    def update_assignment_request_by_id(assignment_request_id: int, req: ModifiedAssignmentRequest, assert_user_authorized: Callable[[int], None]) -> AssignmentRequestView:
        with Session(StorageService.engine) as session:
            assignment_request = session.query(AssignmentRequest).filter_by(
                id=assignment_request_id
            ).first()
            if not assignment_request:
                raise HTTPException(
                    status_code=404,
                    detail="Assignment request not found"
                )
            
            # Check if the user is the owner of the assignment
            assert_user_authorized(assignment_request.tutor_id)

            # Update the assignment request
            assignment_request.requested_rate_hourly = req.requested_rate_hourly or assignment_request.requested_rate_hourly
            assignment_request.requested_duration = req.requested_duration or assignment_request.requested_duration

            StorageService.delete(session, {"assignment_request_id": assignment_request.id}, AssignmentSlot)

            # Add new slots
            for slot in req.available_slots:
                assignment_slot = StorageService.insert(session, AssignmentSlot(
                    day=slot.day,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    assignment_request_id=assignment_request.id
                ))
                session.add(assignment_slot)
            
            session.commit()
            session.refresh(assignment_request, ["assignment"])

            # Send a chat message to the assignment owner
            assignment = assignment_request.assignment
            chat = ChatLogic.get_or_create_private_chat(assignment.owner_id, assignment_request.tutor_id)
            chat_id = chat.id
            
            message_content = json.dumps({
                "hourlyRate": assignment_request.requested_rate_hourly,
                "lessonDuration": assignment_request.requested_duration,
                "assignmentRequestId": assignment_request.id,
                "assignmentId": assignment.id,
                "tutorId": assignment_request.tutor_id,
                "assignmentTitle": assignment.title,
                "availableSlots": [
                    {"day": s.day, "startTime": s.start_time, "endTime": s.end_time}
                    for s in assignment_request.available_slots
                ]
            })
            
            new_chat_message = NewChatMessage(
                chat_id=chat_id,
                content=message_content,
                message_type="tutor_request"
            )

            # Store the chat message and get the message ID
            chat_message = ChatLogic.store_private_message(session, new_chat_message, assignment_request.tutor_id)
            
            # Update the assigment request with the chat message ID
            assignment_request.chat_message_id = chat_message.id
            session.commit()
            session.refresh(chat_message, ["chat", "sender", "assignment_request"])

            print("Sending chat message to assignment owner")
            # Handle the private message asynchronously
            asyncio.create_task(ChatLogic.send_private_message(chat_message=chat_message))
 
            return AssignmentLogic.get_assignment_request_by_id(assignment_request.id, assert_user_authorized)