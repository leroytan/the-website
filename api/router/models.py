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