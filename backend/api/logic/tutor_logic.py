from api.logic.filter_logic import FilterLogic
from api.router.models import (NewTutorProfile, SearchQuery, TutorProfile,
                               TutorPublicSummary)
from api.storage.models import Level, SpecialSkill, Subject, Tutor, User
from api.storage.storage_service import StorageService
from fastapi import HTTPException
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, aliased


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
            photoUrl=tutor.photoUrl,
            rate=tutor.rate,
            rating=tutor.rating,
            subjectsTeachable=subject_names,
            levelsTeachable=level_names,
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
            photoUrl=tutor.photoUrl,
            highestEducation=tutor.highestEducation,
            rate=tutor.rate,
            location=tutor.location,
            rating=tutor.rating,
            aboutMe=tutor.aboutMe,
            subjectsTeachable=subject_names,
            levelsTeachable=level_names,
            specialSkills=[skill.name for skill in tutor.specialSkills] if tutor.specialSkills else [],
            resumeUrl=tutor.resumeUrl,
            experience=tutor.experience,
            availability=tutor.availability,
        )

    @staticmethod
    def search_tutors(search_query: SearchQuery) -> list[TutorPublicSummary]:

        with Session(StorageService.engine) as session:
            filters = []

            user_alias = aliased(User)  # You'll need to import your User model
            statement = session.query(Tutor).join(user_alias, Tutor.user)

            # General search (matching name, location, or aboutMe)
            if search_query.query:
                general_query = f"%{search_query.query}%"  # SQL LIKE pattern
                filters.append(or_(
                    user_alias.name.ilike(general_query),
                    Tutor.location.ilike(general_query),
                    Tutor.aboutMe.ilike(general_query)
                ))

            # get filters from the search query
            parsed_filters = FilterLogic.parse_filters(search_query.filters)

            # Filter by subjects
            if "subject" in parsed_filters:
                filters.append(Tutor.subjects.any(Subject.id.in_(parsed_filters["subject"])))

            # Filter by special skills
            if "specialSkill" in parsed_filters:
                filters.append(Tutor.specialSkills.any(SpecialSkill.id.in_(parsed_filters["specialSkill"])))

            # Filter by levels
            if "level" in parsed_filters:
                filters.append(Tutor.levels.any(Level.id.in_(parsed_filters["level"])))

            statement = statement.filter(and_(*filters))

            tutors = StorageService.find(session, statement, Tutor)

            # Convert the list of Tutor objects to TutorPublicSummary objects            
            summaries = [TutorLogic.convert_tutor_to_public_summary(session, tutor) for tutor in tutors]

            return summaries
    
    @staticmethod
    def new_tutor(tutor_profile: NewTutorProfile, user_id: str|int) -> TutorProfile:
    
        with Session(StorageService.engine) as session:

            tutor_dict = tutor_profile.model_dump()

            tutor_dict.pop("subjectsTeachable", None)
            tutor_dict.pop("levelsTeachable", None)
            tutor_dict.pop("specialSkills", None)

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
            tutor.subjects = session.query(Subject).filter(Subject.name.in_(tutor_profile.subjectsTeachable)).all()
            tutor.levels = session.query(Level).filter(Level.name.in_(tutor_profile.levelsTeachable)).all()
            tutor.specialSkills = session.query(SpecialSkill).filter(SpecialSkill.name.in_(tutor_profile.specialSkills)).all()
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
    def update_profile(tutor_profile: TutorProfile, id: str | int) -> TutorProfile:

        with Session(StorageService.engine) as session:
            # Find the existing tutor profile
            if not StorageService.find(session, {"id": id}, Tutor, find_one=True):
                raise HTTPException(
                    status_code=404,
                    detail="Tutor not found"
                )

            tutor_dict = tutor_profile.model_dump()

            tutor_dict.pop("id", None)
            tutor_dict.pop("subjectsTeachable", None)
            tutor_dict.pop("levelsTeachable", None)
            tutor_dict.pop("specialSkills", None)

            # TODO: settle the update logic to update User and Tutor
            user_dict = {
                "name": tutor_dict["name"],
                "email": tutor_dict["email"]
            }
            StorageService.update(session, {"id": id}, user_dict, User)
            
            tutor_dict.pop("name")
            tutor_dict.pop("email")
            updated_tutor = StorageService.update(session, {"id": id}, tutor_dict, Tutor)

            session.add(updated_tutor)

            # Fetch the related Subject, Level, and SpecialSkill objects
            updated_tutor.subjects = session.query(Subject).filter(Subject.name.in_(tutor_profile.subjectsTeachable)).all()
            updated_tutor.levels = session.query(Level).filter(Level.name.in_(tutor_profile.levelsTeachable)).all()
            updated_tutor.specialSkills = session.query(SpecialSkill).filter(SpecialSkill.name.in_(tutor_profile.specialSkills)).all()
            session.commit()
            session.refresh(updated_tutor)

            return TutorLogic.convert_tutor_to_profile(session, updated_tutor)
