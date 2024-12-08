from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, ARRAY, String, create_engine, Session, select
from sqlalchemy.sql.schema import Column
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr, constr


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, nullable=False)
    name: str
    password_hash: str
    user_type: str # constr(regex="^(tutor|tutee)$")  # Only "tutor" or "tutee"


class Tutor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    education_level: str
    resume: Optional[str]  # Store file path or a URL
    rate: float = Field(ge=0)  # Ensure rate is non-negative
    phone_number: str
    subjects: List[str] = Field(default_factory=list, sa_column=Column(ARRAY(String)))  # Store subjects as JSON array

    user: Optional["User"] = Relationship(back_populates="tutor")


class Tutee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    school: str
    level: str
    subjects: List[str] = Field(default_factory=list, sa_column=Column(ARRAY(String)))  # Store subjects as JSON array
    address: str

    user: Optional["User"] = Relationship(back_populates="tutee")


class User(UserBase, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[str] = Field(default=None)  # Add created_at timestamp
    updated_at: Optional[str] = Field(default=None)  # Add updated_at timestamp

    # One-to-one relationships with Tutor and Tutee
    tutor: Optional[Tutor] = Relationship(back_populates="user")
    tutee: Optional[Tutee] = Relationship(back_populates="user")
