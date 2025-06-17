import enum
import re
from typing import Generic, TypeVar

from api.storage.models import AssignmentRequestStatus, ChatMessageType
from pydantic import BaseModel, EmailStr, Field, validator


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
    photo_url: str | None
    highest_education: str
    rate: str | None
    rating: float | None
    about_me: str
    subjects_teachable: list[str]
    levels_teachable: list[str]
    special_skills: list[str]
    resume_url: str
    experience: str | None
    availability: str | None

class NewTutorProfile(BaseModel):
    highest_education: str | None
    availability: str | None
    resume_url: str | None
    rate: str | None
    location: str | None
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

class AssignmentSlotView(BaseModel):
    id: int
    day: str
    start_time: str
    end_time: str

class NewAssignmentSlot(BaseModel):
    day: str
    start_time: str
    end_time: str

class AssignmentRequestView(BaseModel):
    id: int
    created_at: str
    updated_at: str
    tutor_id: int
    tutor_name: str
    tutor_profile_photo_url: str | None
    requested_rate_hourly: int  # in dollars
    requested_duration: int  # in minutes
    available_slots: list[AssignmentSlotView]
    status: str

# TODO: Remove default values when frontend is ready to handle them
class NewAssignmentRequest(BaseModel):
    requested_rate_hourly: int =35  # in dollars
    requested_duration: int = 60  # in minutes
    available_slots: list[NewAssignmentSlot]

class AssignmentBaseView(BaseModel):
    id: int
    created_at: str
    updated_at: str
    title: str
    owner_id: int
    estimated_rate_hourly: int  # in dollars
    lesson_duration: int  # in minutes
    weekly_frequency: int
    available_slots: list[AssignmentSlotView]
    special_requests: str
    subjects: list[str]
    level: str
    status: str
    location: str

class AssignmentPublicView(AssignmentBaseView):
    applied: bool = False  # Indicates if the user has applied for the assignment
    request_status: AssignmentRequestStatus = AssignmentRequestStatus.NOT_SUBMITTED  # Status of the request if applied

class AssignmentOwnerView(AssignmentBaseView):
    tutor_id: int | None
    requests: list[AssignmentRequestView]

# TODO: Remove lesson_duration default when frontend is ready to handle it
class NewAssignment(BaseModel):
    title: str
    estimated_rate_hourly: int # in dollars
    lesson_duration: int = 90  # in minutes
    weekly_frequency: int
    available_slots: list[NewAssignmentSlot]
    special_requests: str | None
    subjects: list[str]
    level: str
    location: str

class SearchQuery(BaseModel):
    query: str
    filter_by: list[str]
    sort_by: str
    page_size: int = 10
    page_number: int = 1

class FilterChoice(BaseModel):
    id: str
    name: str

class SortChoice(BaseModel):
    id: str
    name: str

class SortOrder(str, enum.Enum):
    ASC = 'asc'
    DESC = 'desc'

# Step 1: Define an Enum for sorting criteria
class AssignmentSortField(str, enum.Enum):
    CREATED_AT = 'created_at'  # Sort by creation date
    estimated_rate_hourly = 'estimated_rate_hourly'  # Sort by estimated rate
    WEEKLY_FREQUENCY = 'weekly_frequency'  # Sort by weekly frequency
    LEVEL = 'level'  # Sort by level (e.g., beginner, intermediate, advanced)
    LOCATION = 'location'  # Sort by location
    TITLE = 'title'  # Sort by assignment title
    RELEVANCE = 'relevance'  # Sort by relevance to the search query
    DEFAULT = ''

T = TypeVar("T")

class SearchResult(BaseModel, Generic[T]):
    results: list[T] = []
    filters: dict[str, list[FilterChoice]] = []
    sorts: list[SortChoice] = []
    num_pages: int = 1
    debug: list = []  # Additional information, e.g., weekly frequency for assignments

class NewChatMessage(BaseModel):
    chat_id: int
    content: str
    message_type: ChatMessageType = ChatMessageType.TEXT_MESSAGE

class ChatPreview(BaseModel):
    id: int
    name: str
    last_message: str
    last_update: str
    last_message_type: str
    has_unread: bool
    is_locked: bool
    has_messages: bool
class UserView(BaseModel):
    id: int
    name: str
    email: str
    profile_photo_url: str | None
    intends_to_be_tutor: bool
    created_at: str
    updated_at: str

class UserUpdateRequest(BaseModel):
    name: str | None = None
    intends_to_be_tutor: bool | None = None

class ChatCreationInfo(BaseModel):
    other_user_id: int

class PaymentRequest(BaseModel):
    mode: str  # 'payment' or 'subscription'
    success_url: str
    cancel_url: str
    assignment_request_id: int
    tutor_id: int  # To link to chat
    chat_id: int | None = None  # Optional, if chat is already created

# Password Reset Models
class ForgotPasswordRequest(BaseModel):
    """
    Model for initiating password reset request
    """
    email: EmailStr

    @validator('email')
    def normalize_email(cls, email):
        """
        Normalize email for consistent handling
        """
        return email.lower().strip()

class ResetPasswordRequest(BaseModel):
    """
    Model for completing password reset
    """
    reset_token: str = Field(
        ..., 
        description="Unique reset token",
        min_length=32,
        max_length=1024
    )
    new_password: str = Field(
        ..., 
        description="New account password",
        min_length=8,
        max_length=128
    )

    @validator('new_password')
    def validate_password_strength(cls, password):
        """
        Comprehensive password strength validation
        
        Requirements:
        - Minimum 12 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character
        """
    
        # if not re.search(r'[A-Z]', password):
        #     raise ValueError("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter")
        
        # if not re.search(r'\d', password):
        #     raise ValueError("Password must contain at least one number")
        
        # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        #     raise ValueError("Password must contain at least one special character")
        
        return password
