import datetime
import enum

from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String, UniqueConstraint)
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
    password_hash = Column(String, nullable=False)

    tutor_role = relationship('Tutor', back_populates='user', uselist=False)

#TODO: Decide which fields in tutor are required and which are optional
class Tutor(Base):
    """Tutor-specific role model"""
    __tablename__ = 'Tutor'
    
    id = Column(Integer, ForeignKey('User.id'), primary_key=True)
    
    # Tutor-specific fields
    photo_url = Column(String, nullable=True)
    highest_education = Column(String, nullable=True)
    availability = Column(String, nullable=True)
    resume_url = Column(String, nullable=True)
    rate = Column(String, nullable=True)
    location = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    about_me = Column(String, nullable=True)
    experience = Column(String, nullable=True)
    
    # Relationships
    subjects = relationship('Subject', secondary='TutorSubject', back_populates='tutors')
    levels = relationship('Level', secondary='TutorLevel', back_populates='tutors')
    special_skills = relationship('SpecialSkill', secondary='TutorSpecialSkill', back_populates='tutors')
    user = relationship('User', back_populates='tutor_role')

class AssignmentStatus(enum.Enum):
    """
    Enum for assignment status
    """
    OPEN = 'OPEN'
    FILLED = 'FILLED'

class Assignment(Base, SerializerMixin):
    """
    Assignment model
    """
    __tablename__ = 'Assignment'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, default=datetime.datetime.now)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('User.id'))  # Foreign key to User
    tutor_id = Column(Integer, ForeignKey('Tutor.id'), nullable=True)  # Foreign key to Tutor
    estimated_rate = Column(String, nullable=False)
    weekly_frequency = Column(Integer, nullable=False)
    special_requests = Column(String, nullable=True)
    status = Column(ENUM(AssignmentStatus), default=AssignmentStatus.OPEN)

    # Relationships
    owner = relationship('User', foreign_keys=[owner_id])
    tutor = relationship('Tutor', foreign_keys=[tutor_id])
    subjects = relationship('Subject', secondary='AssignmentSubject', back_populates='assignments')
    levels = relationship('Level', secondary='AssignmentLevel', back_populates='assignments')
    assignment_requests = relationship('AssignmentRequest', back_populates='assignment')
    available_slots = relationship('AssignmentSlot', back_populates='assignment', primaryjoin="Assignment.id == AssignmentSlot.assignment_id")


class AssignmentSlot(Base):
    """
    Assignment Slot model
    """
    __tablename__ = 'AssignmentSlot'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey('Assignment.id'))  # Foreign key to Assignment
    assignment = relationship('Assignment', back_populates='available_slots')
    day = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)

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
    assignment_id = Column(Integer, ForeignKey('Assignment.id'))  # Foreign key to Assignment
    datetime = Column(DateTime, default=datetime.datetime.now)
    tutor_id = Column(Integer, ForeignKey('Tutor.id'))  # Foreign key to Tutor
    status = Column(ENUM(AssignmentRequestStatus), default=AssignmentRequestStatus.PENDING)

    # Relationships
    tutor = relationship('Tutor', foreign_keys=[tutor_id])
    assignment = relationship('Assignment', foreign_keys=[assignment_id], back_populates='assignment_requests')

    # Constraints
    # Composite unique constraint on column1 and column2
    __table_args__ = (
        UniqueConstraint('assignment_id', 'tutor_id', name='uix_assignment_id_tutor_id'),
    )

class SpecialSkill(Base):
    """
    SpecialSkill model
    """
    __tablename__ = 'SpecialSkill'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    tutors = relationship('Tutor', secondary='TutorSpecialSkill', back_populates='special_skills')

class TutorSpecialSkill(Base):
    __tablename__ = "TutorSpecialSkill"

    id = Column(Integer, primary_key=True)
    tutor_id = Column(Integer, ForeignKey('Tutor.id'))
    special_skill_id = Column(Integer, ForeignKey('SpecialSkill.id'))

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
    tutor_id = Column(Integer, ForeignKey('Tutor.id'))
    subjectId = Column(Integer, ForeignKey('Subject.id'))

class AssignmentSubject(Base):
    __tablename__ = "AssignmentSubject"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('Assignment.id'))
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
    tutor_id = Column(Integer, ForeignKey('Tutor.id'))
    level_id = Column(Integer, ForeignKey('Level.id'))

class AssignmentLevel(Base):
    __tablename__ = "AssignmentLevel"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('Assignment.id'))
    level_id = Column(Integer, ForeignKey('Level.id'))

class ChatMessage(Base, SerializerMixin):
    """
    ChatMessage model
    """
    __tablename__ = 'ChatMessage'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('User.id'))  # Foreign key to User
    receiver_id = Column(Integer, ForeignKey('User.id'))  # Foreign key to User
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    isRead = Column(Boolean, default=False)
    chatroom_id = Column(Integer, ForeignKey('ChatRoom.id'))  # Foreign key to ChatRoom

    # Relationships
    sender = relationship('User', foreign_keys=[sender_id])
    receiver = relationship('User', foreign_keys=[receiver_id])
    chatRoom = relationship('ChatRoom', back_populates='messages')


class ChatRoom(Base):
    """
    ChatRoom model
    """
    __tablename__ = 'ChatRoom'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    user1_id = Column(Integer, ForeignKey('User.id'))  # Foreign key to User
    user2_id = Column(Integer, ForeignKey('User.id'))  # Foreign key to User
    isLocked = Column(Boolean, default=True)

    # Relationships
    user1 = relationship('User', foreign_keys=[user1_id])
    user2 = relationship('User', foreign_keys=[user2_id])
    messages = relationship('ChatMessage', back_populates='chatRoom')
