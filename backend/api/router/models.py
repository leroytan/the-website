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

class CreatedTutorProfile(BaseModel):
    id: int
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

class Assignment(BaseModel):
    id: int
    datetime: str
    requesterId: int
    tutorId: int
    estimatedRate: str
    weeklyFrequency: int
    availableSlots: list[str]
    specialRequests: str | None
    status: str
    
class SearchQuery(BaseModel):
    query: str | None
    filters: list[str] | None
    sorts: list[str] | None
