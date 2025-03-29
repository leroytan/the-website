from api.router.models import TutorProfile, TutorSearchQuery
from api.storage.models import Level, SpecialSkill, Subject, Tutor, UserType
from api.storage.storage_service import StorageService
from sqlalchemy import or_
from sqlalchemy.orm import Session


class TutorLogic:

    @staticmethod
    def search_tutors(search_query: TutorSearchQuery):

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

            # Filter by subjects
            if search_query.subjects:
                filters.append(Tutor.subjects.any(Subject.name.in_(search_query.subjects)))

            # Filter by levels
            if search_query.levels:
                filters.append(Tutor.levels.any(Level.name.in_(search_query.levels)))

        return StorageService.find(session, filters, Tutor)
        query_dict = {
            "general": search_query.query,  # TODO: perform some object transformation; query -> name, address, description????
            "subjects": search_query.subjects,
            "levels": search_query.levels,
        }
        
        # TODO: transform the query dict into a valid query

        with Session(StorageService.engine) as session:
            return StorageService.find(session, query_dict, Tutor)
    
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

