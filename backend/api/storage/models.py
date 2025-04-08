import datetime
import enum

from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String, Table)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_serializer import SerializerMixin

# Create a base class for declarative models
Base = declarative_base()

class User(Base, SerializerMixin):
    """Base User model"""
    __tablename__ = 'User'

    # Core user fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    passwordHash = Column(String, nullable=False)

    tutorRole = relationship('Tutor', back_populates='user', uselist=False)

#TODO: Decide which fields in tutor are required and which are optional
class Tutor(Base):
    """Tutor-specific role model"""
    __tablename__ = 'Tutor'
    
    id = Column(Integer, ForeignKey('User.id'), primary_key=True)
    
    # Tutor-specific fields
    photoUrl = Column(String, nullable=True)
    highestEducation = Column(String, nullable=True)
    availability = Column(String, nullable=True)
    resumeUrl = Column(String, nullable=True)
    rate = Column(String, nullable=True)
    location = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    aboutMe = Column(String, nullable=True)
    experience = Column(String, nullable=True)
    
    # Relationships
    subjects = relationship('Subject', secondary='TutorSubject', back_populates='tutors')
    levels = relationship('Level', secondary='TutorLevel', back_populates='tutors')
    specialSkills = relationship('SpecialSkill', secondary='TutorSpecialSkill', back_populates='tutors')
    user = relationship('User', back_populates='tutorRole')
    
class TutorRequestStatus(enum.Enum):
    """Enum for tutor request status"""
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'

class TutorRequest(Base):
    """Tutor Request model"""
    __tablename__ = 'TutorRequest'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, default=datetime.datetime.now)
    requesterId = Column(Integer, ForeignKey('User.id'))  # Foreign key to requester
    tutorId = Column(Integer, ForeignKey('Tutor.id'))  # Foreign key to tutor
    status = Column(ENUM(TutorRequestStatus), default=TutorRequestStatus.PENDING)

    # Relationships
    requester = relationship('User', foreign_keys=[requesterId])
    tutor = relationship('Tutor', foreign_keys=[tutorId])

class AssignmentStatus(enum.Enum):
    """
    Enum for assignment status
    """
    OPEN = 'OPEN'
    FILLED = 'FILLED'

class Assignment(Base):
    """
    Assignment model
    """
    __tablename__ = 'Assignment'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(String, nullable=False)
    requesterId = Column(Integer, ForeignKey('User.id'))  # Foreign key to User
    tutorId = Column(Integer, ForeignKey('Tutor.id'))  # Foreign key to Tutor
    estimatedRate = Column(String, nullable=False)
    weeklyFrequency = Column(Integer, nullable=False)
    specialRequests = Column(String, nullable=True)
    status = Column(ENUM(AssignmentStatus), default=AssignmentStatus.OPEN)

    # Relationships
    requester = relationship('User', foreign_keys=[requesterId])
    tutor = relationship('Tutor', foreign_keys=[tutorId])
    subjects = relationship('Subject', secondary='AssignmentSubject', back_populates='assignments')
    levels = relationship('Level', secondary='AssignmentLevel', back_populates='assignments')
    assignmentRequests = relationship('AssignmentRequest', back_populates='assignment')
    availableSlots = relationship('AssignmentSlot', back_populates='assignment', primaryjoin="Assignment.id == AssignmentSlot.assignmentId")


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

class AssignmentRequestStatus(enum.Enum):
    """
    Enum for assignment request status
    """
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'

class AssignmentRequest(Base):
    """
    Assignment Request model
    """
    __tablename__ = 'AssignmentRequest'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    assignmentId = Column(Integer, ForeignKey('Assignment.id'))  # Foreign key to Assignment
    datetime = Column(DateTime, default=datetime.datetime.now)
    tutorId = Column(Integer, ForeignKey('Tutor.id'))  # Foreign key to Tutor
    status = Column(ENUM(AssignmentRequestStatus), default=AssignmentRequestStatus.PENDING)

    # Relationships
    tutor = relationship('Tutor', foreign_keys=[tutorId])
    assignment = relationship('Assignment', foreign_keys=[assignmentId], back_populates='assignmentRequests')

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
    tutorId = Column(Integer, ForeignKey('Tutor.id'))
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
    assignments = relationship('Assignment', secondary='AssignmentSubject', back_populates='subjects')

    @hybrid_property
    def filterId(self):
        """
        Returns the filter ID for the subject
        """
        return f"subject_{self.id}"
    
class TutorSubject(Base):
    __tablename__ = "TutorSubject"

    id = Column(Integer, primary_key=True)
    tutorId = Column(Integer, ForeignKey('Tutor.id'))
    subjectId = Column(Integer, ForeignKey('Subject.id'))

class AssignmentSubject(Base):
    __tablename__ = "AssignmentSubject"

    id = Column(Integer, primary_key=True)
    assignmentId = Column(Integer, ForeignKey('Assignment.id'))
    subjectId = Column(Integer, ForeignKey('Subject.id'))

class Level(Base):
    """
    Level model
    """
    __tablename__ = 'Level'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    tutors = relationship('Tutor', secondary='TutorLevel', back_populates='levels')
    assignments = relationship('Assignment', secondary='AssignmentLevel', back_populates='levels')

    @hybrid_property
    def filterId(self):
        """
        Returns the filter ID for the level
        """
        return f"level_{self.id}"
    
class TutorLevel(Base):
    __tablename__ = "TutorLevel"

    id = Column(Integer, primary_key=True)
    tutorId = Column(Integer, ForeignKey('Tutor.id'))
    levelId = Column(Integer, ForeignKey('Level.id'))

class AssignmentLevel(Base):
    __tablename__ = "AssignmentLevel"

    id = Column(Integer, primary_key=True)
    assignmentId = Column(Integer, ForeignKey('Assignment.id'))
    levelId = Column(Integer, ForeignKey('Level.id'))


