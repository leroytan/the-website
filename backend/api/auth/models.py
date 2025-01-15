from pydantic import BaseModel

from api.storage.models import UserType

class TokenData(BaseModel):
    email: str
    userType: UserType