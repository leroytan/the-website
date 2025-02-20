from api.router.models import ClientProfile


class ClientLogic:

    @staticmethod
    def find_client_by_id(id: str) -> ClientProfile | None:
        client = ClientProfile.objects(id=id).first()
        return client
    
    @staticmethod
    def update_client_profile(data: dict) -> ClientProfile:
        
        return None