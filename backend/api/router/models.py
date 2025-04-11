from typing import Generic, TypeVar

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
    photoUrl: str | None
    rate: str | None
    rating: float | None
    subjectsTeachable: list[str]
    levelsTeachable: list[str]
    experience: str | None
    availability: str | None

class NewTutorProfile(BaseModel):
    photoUrl: str | None
    highestEducation: str | None
    availability: str | None
    resumeUrl: str | None
    rate: str | None
    location: str | None
    rating: float | None
    aboutMe: str | None
    experience: str | None
    subjectsTeachable: list[str]
    levelsTeachable: list[str]
    specialSkills: list[str]

#TODO: Decide which fields in tutor are required and which are optional
class TutorProfile(BaseModel):
    id: int
    name: str
    email: str
    photoUrl: str | None
    highestEducation: str | None
    rate: str | None
    location: str | None
    rating: float | None
    aboutMe: str | None
    subjectsTeachable: list[str]
    levelsTeachable: list[str]
    specialSkills: list[str]
    resumeUrl: str | None
    experience: str | None
    availability: str | None

class ClientTutorRequest(BaseModel):
    id: str
    tutorId: int
    requesterId: int
    datetime: str
    status: str

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

class AssignmentSlot(BaseModel):
    id: int
    day: str
    startTime: str
    endTime: str

class Assignment(BaseModel):
    id: int
    datetime: str
    title: str
    requesterId: int
    tutorId: int | None
    estimatedRate: str
    weeklyFrequency: int
    availableSlots: list[AssignmentSlot]
    specialRequests: str | None
    subjects: list[str]
    levels: list[str]
    status: str

class NewAssignment(BaseModel):
    title: str
    estimatedRate: str
    weeklyFrequency: int
    availableSlots: list[AssignmentSlot]
    specialRequests: str | None
    subjects: list[str]
    levels: list[str]

class SearchQuery(BaseModel):
    query: str | None
    filters: list[str] | None
    sorts: list[str] | None

T = TypeVar("T")

class SearchResult(BaseModel, Generic[T]):
    results: list[T]
    filters: dict[str, list[dict[str, str]]]

class NewChatMessage(BaseModel):
    receiverId: int
    content: str