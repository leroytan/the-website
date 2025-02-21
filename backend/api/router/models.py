from typing import List, Optional

from api.storage.models import UserType
from pydantic import BaseModel


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
    photoUrl: str | None
    rate: float | None
    rating: int | None
    subjectsTeachable: list[str]
    levelsTeachable: list[str]
    experience: str | None
    availability: str | None

class TutorProfile(BaseModel):
    id: int
    name: str
    contact: str
    email: str
    photoUrl: str | None
    highestEducation: str | None
    rate: float | None
    location: str | None
    rating: int | None
    aboutMe: str | None
    subjectsTeachable: list[str]
    levelsTeachable: list[str]
    specialSkills: list[str]
    resumeUrl: str | None
    experience: str | None
    availability: str | None
    isProfileComplete: bool

class ClientTutorRequest(BaseModel):
    id: str
    tutorId: int
    clientId: int
    datetime: str
    status: str

class TutorSearchQuery(BaseModel):
    query: str
    subjects: list[str]
    levels: list[str]
    
class CoursePublicSummary(BaseModel):
    id: str
    name: str
    description: str
    progress: float
    fileLink: str | None

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

class ClientProfile(BaseModel):
    id: int
    name: str
    school: str | None
    level: str | None
    subjects: list[str]
    contact: str
    email: str
    isProfileComplete: bool

class Assignment(BaseModel):
    id: int
    clientId: int
    tutorId: int
    weeklyFrequency: int
    availableSlots: list[str]
    datetime: str
    specialRequests: str | None
    status: str
    