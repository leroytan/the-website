import enum

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base, relationship

# Create a base class for declarative models
Base = declarative_base()

# Enum for user types
class UserType(enum.Enum):
    """
    Enum for user types
    """
    CLIENT = 'CLIENT'
    TUTOR = 'TUTOR'

# Singular models
# Single table inheritance for User model
class User(Base):
    """
    Base User model with composite primary key of email and userType
    """
    __tablename__ = 'User'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    userType = Column(ENUM(UserType), nullable=False)
    password_hash = Column(String, nullable=False)

    # Discriminator column for inheritance
    @declared_attr
    def __mapper_args__(cls):
        if cls.__name__ == 'User':
            return {
                "polymorphic_identity": "user",
                "polymorphic_on": cls.userType
            }
        return {}

class Client(User):
    """
    Client-specific user model
    """
    
    # Specific fields for Client
    client_specific_field = Column(String, nullable=True)

    # Mapper args for inheritance
    __mapper_args__ = {
        "polymorphic_identity": UserType.CLIENT
    }

class Tutor(User):
    """
    Tutor-specific user model
    """

    # Specific fields for Tutor
    photoUrl = Column(String, nullable=True)
    rate = Column(Float, nullable=True)
    rating = Column(Integer, nullable=True)
    experience = Column(String, nullable=True)
    availability = Column(String, nullable=True)

    subjects = relationship('Subject', secondary='TutorSubject', back_populates='tutors')

    # Mapper args for inheritance
    __mapper_args__ = {
        "polymorphic_identity": UserType.TUTOR
    }

class Subject(Base):
    """
    Subject model
    """
    __tablename__ = 'Subject'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    tutors = relationship('Tutor', secondary='TutorSubject', back_populates='subjects')

class TutorSubject(Base):
    __tablename__ = "TutorSubject"

    id = Column(Integer, primary_key=True)
    tutor_id = Column(Integer, ForeignKey('User.id'))
    subject_id = Column(Integer, ForeignKey('Subject.id'))


# Many-to-many relationship tables

# # Define the association tables
# class TutorSubject(Base):
#     """
#     Association table for Tutor and Subject
#     """
#     __tablename__ = 'TutorSubject'

#     # Columns
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     tutorId = Column(Integer, ForeignKey('User.id'))
#     subjectId = Column(Integer, ForeignKey('Subject.id'))

#     tutor = relationship("Tutor", back_populates="subjects")
#     subject = relationship("Subject")

# class TutorLevel(Base):
#     """
#     Association table for Tutor and Level
#     """
#     __tablename__ = 'TutorLevel'

#     # Columns
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     tutorId = Column(Integer, ForeignKey('User.id'))
#     levelId = Column(Integer, ForeignKey('Level.id'))

#     tutor = relationship("Tutor", back_populates="levels")
#     level = relationship("Level")


    