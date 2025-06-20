import math

from api.logic.filter_logic import FilterLogic
from api.logic.user_logic import UserLogic
from api.router.models import (NewTutorProfile, SearchQuery, TutorProfile,
                               TutorPublicSummary)
from api.storage.models import Level, SpecialSkill, Subject, Tutor, User
from api.storage.storage_service import StorageService
from fastapi import HTTPException
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, aliased, selectinload


class TutorLogic:

    @staticmethod
    def convert_tutor_to_public_summary(session: Session, tutor: Tutor) -> TutorPublicSummary:
        """
        Converts a Tutor model instance to a TutorPublicSummary model.
        
        Args:
            tutor: A Tutor model instance
            
        Returns:
            TutorPublicSummary: A pydantic model with the public tutor information
        """
        tutor = session.merge(tutor)

        # Extract subject and level names
        subject_names = [subject.name for subject in tutor.subjects] if tutor.subjects else []
        level_names = [level.name for level in tutor.levels] if tutor.levels else []
        
        # Create and return the TutorPublicSummary
        return TutorPublicSummary(
            id=tutor.id,
            name=tutor.user.name,
            photo_url=UserLogic.get_profile_photo_url(tutor.id),
            highest_education=tutor.highest_education,
            rate=tutor.rate,
            rating=tutor.rating,
            about_me=tutor.about_me,
            subjects_teachable=subject_names,
            levels_teachable=level_names,
            special_skills=[skill.name for skill in tutor.special_skills] if tutor.special_skills else [],
            resume_url=tutor.resume_url,
            experience=tutor.experience,
            availability=tutor.availability
        )
    
    @staticmethod
    def convert_tutor_to_profile(session: Session, tutor: Tutor) -> TutorProfile:
        """
        Converts a Tutor model instance to a TutorProfile model.
        
        Args:
            tutor: A Tutor model instance
            
        Returns:
            TutorProfile: A pydantic model with the full tutor information
        """
        tutor = session.merge(tutor)

        # Extract subject and level names
        subject_names = [subject.name for subject in tutor.subjects] if tutor.subjects else []
        level_names = [level.name for level in tutor.levels] if tutor.levels else []
        
        # Create and return the TutorProfile
        return TutorProfile(
            id=tutor.id,
            name=tutor.user.name,
            contact=tutor.user.email,
            email=tutor.user.email,
            photo_url=UserLogic.get_profile_photo_url(tutor.id),
            highest_education=tutor.highest_education,
            rate=tutor.rate,
            location=tutor.location,
            rating=tutor.rating,
            about_me=tutor.about_me,
            subjects_teachable=subject_names,
            levels_teachable=level_names,
            special_skills=[skill.name for skill in tutor.special_skills] if tutor.special_skills else [],
            resume_url=tutor.resume_url,
            experience=tutor.experience,
            availability=tutor.availability,
        )

    @staticmethod
    def search_tutors(search_query: SearchQuery) -> list[TutorPublicSummary]:

        with Session(StorageService.engine) as session:
            filters = []

            user_alias = aliased(User)  # You'll need to import your User model
            statement = session.query(Tutor)
            statement = statement.join(user_alias, Tutor.user)

            # General search (matching name, location, or about_me)
            if search_query.query:
                general_query = f"%{search_query.query}%"  # SQL LIKE pattern
                filters.append(or_(
                    user_alias.name.ilike(general_query),
                    Tutor.location.ilike(general_query),
                    Tutor.about_me.ilike(general_query)
                ))

            # get filters from the search query
            parsed_filters = FilterLogic.parse_filters(search_query.filter_by)

            # Filter by subjects
            if "subject" in parsed_filters:
                filters.append(Tutor.subjects.any(Subject.filter_id.in_(parsed_filters["subject"])))

            # Filter by special skills
            if "specialSkill" in parsed_filters:
                filters.append(Tutor.subjects.any(SpecialSkill.filter_id.in_(parsed_filters["special_skill"])))

            # Filter by levels
            if "level" in parsed_filters:
                filters.append(Tutor.levels.any(Level.filter_id.in_(parsed_filters["level"])))

            statement = statement.filter(and_(*filters))
            # Default ordering by rating and name
            # TODO: Allow sorting by other fields
            statement = statement.order_by(Tutor.rating.desc(), user_alias.name.asc())

            # Pagination
            page_size = search_query.page_size
            offset = (search_query.page_number - 1) * page_size
            num_pages = math.ceil(statement.count() / page_size)
            statement = statement.offset(offset).limit(page_size)
            tutors = statement.all()

            # Convert the list of Tutor objects to TutorPublicSummary objects            
            summaries = [TutorLogic.convert_tutor_to_public_summary(session, tutor) for tutor in tutors]

            return {
                "results": summaries,
                "num_pages": num_pages,
            }
    
    @staticmethod
    def new_tutor(tutor_profile: NewTutorProfile, user_id: str|int) -> TutorProfile:
    
        with Session(StorageService.engine) as session:

            tutor_dict = tutor_profile.model_dump()

            tutor_dict.pop("subjects_teachable", None)
            tutor_dict.pop("levels_teachable", None)
            tutor_dict.pop("special_skills", None)

            try:
                tutor = StorageService.insert(session, Tutor(
                    id=user_id,
                    **tutor_dict
                ))
            except IntegrityError as e:
                if isinstance(e.orig, UniqueViolation):
                    raise HTTPException(
                        status_code=409,
                        detail="Tutor with this email already exists"
                    )
                elif isinstance(e.orig, ForeignKeyViolation):
                    raise HTTPException(
                        status_code=409,
                        detail="User with this email does not exist"
                    )
                else:
                    raise HTTPException(
                        status_code=500,
                        detail="Internal server error"
                    )

            session.add(tutor)
            # Fetch the related Subject, Level, and SpecialSkill objects
            tutor.subjects = session.query(Subject).filter(Subject.name.in_(tutor_profile.subjects_teachable)).all()
            tutor.levels = session.query(Level).filter(Level.name.in_(tutor_profile.levels_teachable)).all()
            tutor.special_skills = session.query(SpecialSkill).filter(SpecialSkill.name.in_(tutor_profile.special_skills)).all()
            # tutor.user = StorageService.find(session, {"id": tutor_profile.id}, User, find_one=True)
            session.commit()
            session.refresh(tutor)

            # Convert the Tutor object to a TutorProfile object
            tutor_profile = TutorLogic.convert_tutor_to_profile(session, tutor)
            return tutor_profile
    
    @staticmethod
    def find_profile_by_id(id: str | int, is_self: bool = False) -> TutorPublicSummary | TutorProfile | None:
        with Session(StorageService.engine) as session:
            tutor = StorageService.find(session, {"id": id}, Tutor, find_one=True)

            if not tutor:
                raise HTTPException(
                    status_code=404,
                    detail="Tutor not found"
                )
            
            if not is_self:
                # Convert the Tutor object to a TutorPublicSummary object
                return TutorLogic.convert_tutor_to_public_summary(session, tutor)
            else:
                return TutorLogic.convert_tutor_to_profile(session, tutor)

    @staticmethod
    def update_profile(tutor_profile: NewTutorProfile, id: str | int) -> TutorProfile:

        with Session(StorageService.engine) as session:
            # Find the existing tutor profile
            tutor = session.query(Tutor).options(
                selectinload(Tutor.subjects),
                selectinload(Tutor.levels),
                selectinload(Tutor.special_skills)
            ).filter(Tutor.id == id).first()
            if not tutor:
                raise HTTPException(
                    status_code=404,
                    detail="Tutor not found"
                )

            tutor_dict = tutor_profile.model_dump(exclude_unset=True)

            tutor_dict.pop("subjects_teachable", None)
            tutor_dict.pop("levels_teachable", None)
            tutor_dict.pop("special_skills", None)

            # Update the tutor profile in the database
            for field, updated_value in tutor_dict.items():
                setattr(tutor, field, updated_value)

            # Fetch the related Subject, Level, and SpecialSkill objects
            tutor.subjects = session.query(Subject).filter(Subject.name.in_(tutor_profile.subjects_teachable)).all()
            tutor.levels = session.query(Level).filter(Level.name.in_(tutor_profile.levels_teachable)).all()
            tutor.special_skills = session.query(SpecialSkill).filter(SpecialSkill.name.in_(tutor_profile.special_skills)).all()
            session.commit()
            session.refresh(tutor)

            return TutorLogic.convert_tutor_to_profile(session, tutor)
