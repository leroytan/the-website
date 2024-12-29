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

class TutorSearchQuery(BaseModel):
    query: str
    subjects: list[str]
    levels: list[str]
    
class CoursePublicSummary(BaseModel):
    id: str
    name: str
    description: str
    progress: float
    fileLink: Optional[str]

class CourseModule(BaseModel):
    courseOverview: str
    progress: float
    id: int
    name: str
    completed: bool
    locked: bool
    videoUrl: str

class Reviewer(BaseModel):
    year: int
    course: str
    specialization: str

class Review(BaseModel):
    yearSem: str
    workload: str
    difficulty: int
    overview: str
    otherPoints: str
    reviewer: Reviewer

class Module(BaseModel):
    code: str
    name: str
    reviews: list[Review]

    