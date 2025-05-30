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
    intends_to_be_tutor: bool = False

class TutorPublicSummary(BaseModel):
    id: int
    name: str
    photo_url: Optional[str]
    rate: Optional[float]
    rating: Optional[int]
    subjects_teachable: List[str]
    levels_teachable: List[str]
    experience: Optional[str]
    availability: Optional[str]
