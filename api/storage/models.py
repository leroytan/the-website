from sqlmodel import Field, SQLModel
from typing import Optional
import enum

# Define the UserType enum for better type safety
class UserType(str, enum.Enum):
    client = "client"
    tutor = "tutor"

# Define the User class with composite primary key
class User(SQLModel, table=True):
    email: str = Field(primary_key=True, index=True)
    password_hash: str
    userType: UserType = Field(primary_key=True, index=True)

# Define the Client class which extends User
class Client(User, table=True):
    userType: UserType = UserType.client  # Ensuring this is a client
    client_specific_field: Optional[str] = None  # Add any client-specific fields

# Define the Tutor class which extends User
class Tutor(User, table=True):
    userType: UserType = UserType.tutor  # Ensuring this is a tutor
    tutor_specific_field: Optional[str] = None  # Add any tutor-specific fields