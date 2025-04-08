from typing import List, Optional

from pydantic import BaseModel


# Pydantic models
class LoginRequest(BaseModel):
    email: str
    password: str
    
class SignupRequest(BaseModel):
    email: str
    password: str
    name: str

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
