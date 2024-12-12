from api.storage.storage_service import StorageService

class TutorLogic:

    @staticmethod
    def get_public_summaries():
        return StorageService.find_many_tutors({})
