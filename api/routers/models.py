from pydantic import BaseModel
from typing import List, Optional

# Pydantic models
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str

class LoginPageResponse(BaseModel):
    title: str
    description: str
    fields: list[dict]

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str
    userType: str

class SignupResponse(BaseModel):
    id: str
    email: str
    name: str
    userType: str
    token: str

class HomepageResponse(BaseModel):
    userType: str
    featuredContent: List[dict]

class ProfileResponse(BaseModel):
    id: str
    email: str
    name: str
    userType: str
    profileComplete: bool

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    phoneNumber: Optional[str] = None

class TutorOnboardingRequest(BaseModel):
    subjects: List[str]
    educationLevel: str
    resume: dict
    rate: dict
    phoneNumber: int

class ClientOnboardingRequest(BaseModel):
    school: str
    level: str
    subjects: List[str]
    address: str