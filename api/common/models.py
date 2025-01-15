from pydantic import BaseModel
from typing import List, Optional
from api.storage.models import UserType

# Pydantic models
class LoginRequest(BaseModel):
    email: str
    password: str
    userType: UserType

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str
    userType: UserType

class TutorPublicSummary(BaseModel):
    id: int
    name: str
    photoUrl: Optional[str]
    rate: Optional[float]
    rating: Optional[int]
    subjectsTeachable: List[str]
    levelsTeachable: List[str]
    experience: Optional[str]
    availability: Optional[str]
