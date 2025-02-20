from api.router.models import TutorSearchQuery
from api.storage.storage_service import StorageService


class TutorLogic:

    @staticmethod
    def get_public_summaries():
        return StorageService.get_tutor_summaries()

    @staticmethod
    def search_tutors(search_query: TutorSearchQuery):
        query_dict = {
            "name": search_query.query,  # TODO: perform some object transformation; query -> name, address, description????
            "subjects": search_query.subjects,
            "levels": search_query.levels,
        }
        return StorageService.search_tutors(query_dict)
    
    @staticmethod
    def find_tutor_by_id(tutor_id):  # TODO: transform to tutor public fields before returning
        return StorageService.find_one_tutor({"id": tutor_id})