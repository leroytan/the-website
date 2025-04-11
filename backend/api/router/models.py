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
    photo_url: str | None
    rate: str | None
    rating: float | None
    subjects_teachable: list[str]
    levels_teachable: list[str]
    experience: str | None
    availability: str | None

class NewTutorProfile(BaseModel):
    photo_url: str | None
    highest_education: str | None
    availability: str | None
    resume_url: str | None
    rate: str | None
    location: str | None
    rating: float | None
    about_me: str | None
    experience: str | None
    subjects_teachable: list[str]
    levels_teachable: list[str]
    special_skills: list[str]

#TODO: Decide which fields in tutor are required and which are optional
class TutorProfile(BaseModel):
    id: int
    name: str
    email: str
    photo_url: str | None
    highest_education: str | None
    rate: str | None
    location: str | None
    rating: float | None
    about_me: str | None
    subjects_teachable: list[str]
    levels_teachable: list[str]
    special_skills: list[str]
    resume_url: str | None
    experience: str | None
    availability: str | None

class CoursePublicSummary(BaseModel):
    id: str
    name: str
    description: str
    progress: float
    file_link: str | None

class CourseModule(BaseModel):
    course_overview: str
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
    year_sem: str
    workload: str
    difficulty: int
    overview: str
    otherPoints: str
    reviewer: Reviewer

class Module(BaseModel):
    code: str
    name: str
    reviews: list[Review]

class AssignmentSlot(BaseModel):
    id: int
    day: str
    start_time: str
    end_time: str

class Assignment(BaseModel):
    id: int
    datetime: str
    title: str
    owner_id: int
    tutor_id: int | None
    estimated_rate: str
    weekly_frequency: int
    available_slots: list[AssignmentSlot]
    special_requests: str | None
    subjects: list[str]
    levels: list[str]
    status: str

class NewAssignmentSlot(BaseModel):
    day: str
    start_time: str
    end_time: str

class NewAssignment(BaseModel):
    title: str
    estimated_rate: str
    weekly_frequency: int
    available_slots: list[NewAssignmentSlot]
    special_requests: str | None
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
    receiver_id: int
    content: str