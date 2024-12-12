from api.storage.storage_service import StorageService


class TutorLogic:

    @staticmethod
    def get_all_tutors():
        return StorageService.find_many_tutors({})
