import enum

from sqlalchemy import (Boolean, Column, Float, ForeignKey, Integer, String,
                        Table)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_serializer import SerializerMixin

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
class User(Base, SerializerMixin):
    """
    Base User model with composite primary key of email and userType
    """
    __tablename__ = 'User'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    contact = Column(String, nullable=True)
    userType = Column(ENUM(UserType), nullable=False)
    passwordHash = Column(String, nullable=False)
    isProfileComplete = Column(Boolean, nullable=False, default=False)

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
    school = Column(String, nullable=True)
    level = Column(String, nullable=True)

    subjects = relationship('Subject', secondary='ClientSubject', back_populates='clients')

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
    highestEducation = Column(String, nullable=True)
    availability = Column(String, nullable=True)
    resumeUrl = Column(String, nullable=True)
    rate = Column(String, nullable=True)
    location = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    aboutMe = Column(String, nullable=True)
    experience = Column(String, nullable=True)
    subjects = relationship('Subject', secondary='TutorSubject', back_populates='tutors')
    levels = relationship('Level', secondary='TutorLevel', back_populates='tutors')
    specialSkills = relationship('SpecialSkill', secondary='TutorSpecialSkill', back_populates='tutors')

    # Mapper args for inheritance
    __mapper_args__ = {
        "polymorphic_identity": UserType.TUTOR
    }

class SpecialSkill(Base):
    """
    SpecialSkill model
    """
    __tablename__ = 'SpecialSkill'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    tutors = relationship('Tutor', secondary='TutorSpecialSkill', back_populates='specialSkills')

class TutorSpecialSkill(Base):
    __tablename__ = "TutorSpecialSkill"

    id = Column(Integer, primary_key=True)
    tutorId = Column(Integer, ForeignKey('User.id'))
    specialSkillId = Column(Integer, ForeignKey('SpecialSkill.id'))

class Subject(Base):
    """
    Subject model
    """
    __tablename__ = 'Subject'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    tutors = relationship('Tutor', secondary='TutorSubject', back_populates='subjects')
    clients = relationship('Client', secondary='ClientSubject', back_populates='subjects')

class Level(Base):
    """
    Level model
    """
    __tablename__ = 'Level'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    tutors = relationship('Tutor', secondary='TutorLevel', back_populates='levels')

class AssignmentStatus(enum.Enum):
    """
    Enum for assignment status
    """
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    COMPLETED = 'COMPLETED'

class Assignment(Base):
    """
    Assignment model
    """
    __tablename__ = 'Assignment'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(String, nullable=False)
    clientId = Column(Integer, ForeignKey('User.id'))
    tutorId = Column(Integer, ForeignKey('User.id'), nullable=True)
    subjectId = Column(Integer, ForeignKey('Subject.id'))
    estimatedRate = Column(String, nullable=False)
    weeklyFrequency = Column(Integer, nullable=False)
    availableSlots = relationship('AssignmentSlot', back_populates='assignment', primaryjoin="Assignment.id == AssignmentSlot.assignmentId")
    specialRequests = Column(String, nullable=True)
    status = Column(ENUM(AssignmentStatus), nullable=False)

class AssignmentSlot(Base):
    """
    Assignment Slot model
    """
    __tablename__ = 'AssignmentSlot'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    assignmentId = Column(Integer, ForeignKey('Assignment.id'))  # Foreign key to Assignment
    assignment = relationship('Assignment', back_populates='availableSlots')
    day = Column(String, nullable=False)
    startTime = Column(String, nullable=False)
    endTime = Column(String, nullable=False)

class TutorSubject(Base):
    __tablename__ = "TutorSubject"

    id = Column(Integer, primary_key=True)
    tutorId = Column(Integer, ForeignKey('User.id'))
    subjectId = Column(Integer, ForeignKey('Subject.id'))

class ClientSubject(Base):
    __tablename__ = "ClientSubject"

    id = Column(Integer, primary_key=True)
    clientId = Column(Integer, ForeignKey('User.id'))
    subjectId = Column(Integer, ForeignKey('Subject.id'))

class TutorLevel(Base):
    __tablename__ = "TutorLevel"

    id = Column(Integer, primary_key=True)
    tutorId = Column(Integer, ForeignKey('User.id'))
    levelId = Column(Integer, ForeignKey('Level.id'))

class TutorRequest(Base):
    __tablename__ = "TutorRequest"

    id = Column(Integer, primary_key=True)
    tutorId = Column(Integer, ForeignKey('User.id'))
    clientId = Column(Integer, ForeignKey('User.id'))
    datetime = Column(String, nullable=False)

class AssignmentRequest(Base):
    __tablename__ = "AssignmentRequest"

    id = Column(Integer, primary_key=True)
    assignmentId = Column(Integer, ForeignKey('Assignment.id'))
    tutorId = Column(Integer, ForeignKey('User.id'))
    datetime = Column(String, nullable=False)

    