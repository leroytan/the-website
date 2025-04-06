from api.logic.filter_logic import FilterLogic
from api.router.models import SearchQuery, TutorProfile, TutorPublicSummary
from api.storage.models import Level, SpecialSkill, Subject, Tutor
from api.storage.storage_service import StorageService
from sqlalchemy import or_
from sqlalchemy.orm import Session


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
            name=tutor.name,
            photoUrl=tutor.photoUrl,
            rate=tutor.rate,
            rating=tutor.rating,
            subjectsTeachable=subject_names,
            levelsTeachable=level_names,
            experience=tutor.experience,
            availability=tutor.availability
        )

    @staticmethod
    def search_tutors(search_query: SearchQuery) -> list[TutorPublicSummary]:

        with Session(StorageService.engine) as session:
            filters = []

            # General search (matching name, location, or aboutMe)
            if search_query.query:
                general_query = f"%{search_query.query}%"  # SQL LIKE pattern
                filters.append(or_(
                    Tutor.name.ilike(general_query),
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

            tutors = StorageService.find(session, filters, Tutor)

            if not tutors:
                raise ValueError("No tutors found matching the search criteria.")

            # Convert the list of Tutor objects to TutorPublicSummary objects            
            summaries = [TutorLogic.convert_tutor_to_public_summary(session, tutor) for tutor in tutors]

            return summaries
    
    @staticmethod
    def create_tutor(tutor_profile: TutorProfile):
        # Create a new Tutor instance from the incoming request data
        tutor_dict = tutor_profile.model_dump()

        tutor_dict["isProfileComplete"] = False  # TODO: perform some validation to make it true
        tutor_dict.pop("subjectsTeachable", None)
        tutor_dict.pop("levelsTeachable", None)
        tutor_dict.pop("specialSkills", None)
        tutor_dict.pop("id", None)

        with Session(StorageService.engine) as session:
            tutor = StorageService.update(session, {'email': tutor_profile.email}, tutor_dict, Tutor)
            session.add(tutor)
            # Fetch the related Subject, Level, and SpecialSkill objects
            tutor.subjects = session.query(Subject).filter(Subject.name.in_(tutor_profile.subjectsTeachable)).all()
            tutor.levels = session.query(Level).filter(Level.name.in_(tutor_profile.levelsTeachable)).all()
            tutor.specialSkills = session.query(SpecialSkill).filter(SpecialSkill.name.in_(tutor_profile.specialSkills)).all()
            session.commit()
            session.refresh(tutor)

        return tutor

