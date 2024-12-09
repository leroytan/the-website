from pydantic import BaseModel
from typing import List, Optional

# Pydantic models
class LoginRequest(BaseModel):
    email: str
    password: str
    userType: str

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str
    userType: str