import datetime
import enum

from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, Float,
                        ForeignKey, Integer, String, UniqueConstraint)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin

# Create a base class for declarative models
Decl_Base = declarative_base()

class Base(Decl_Base):
    __abstract__ = True
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class User(Base, SerializerMixin):
    """Base User model"""
    __tablename__ = 'User'

    # Core user fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    intends_to_be_tutor = Column(Boolean, default=False)

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
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('User.id'))  # Foreign key to User
    tutor_id = Column(Integer, ForeignKey('Tutor.id'), nullable=True)  # Foreign key to Tutor
    level_id = Column(Integer, ForeignKey('Level.id'), nullable=False)  # Foreign key to Level
    estimated_rate = Column(String, nullable=False)
    weekly_frequency = Column(Integer, nullable=False)
    special_requests = Column(String, nullable=True)
    location = Column(String, nullable=False)
    status = Column(ENUM(AssignmentStatus), default=AssignmentStatus.OPEN)

    # Relationships
    owner = relationship('User', foreign_keys=[owner_id])
    tutor = relationship('Tutor', foreign_keys=[tutor_id])
    subjects = relationship('Subject', secondary='AssignmentSubject', back_populates='assignments')
    level = relationship('Level', foreign_keys=[level_id], back_populates='assignments')
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
    NOT_SUBMITTED = 'NOT_SUBMITTED'
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
    assignments = relationship('Assignment', back_populates='level')

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
    

class PrivateChat(Base, SerializerMixin):
    __tablename__ = 'PrivateChat'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    user1_id = Column(Integer, ForeignKey('User.id'), nullable=False)  # Foreign key to User
    user2_id = Column(Integer, ForeignKey('User.id'), nullable=False)  # Foreign key to User
    is_locked = Column(Boolean, default=True)

    # TODO: Implement alias names for locked chats
    # user_1_alias = Column(String, nullable=True)
    # user_2_alias = Column(String, nullable=True)

    # Relationships
    user1 = relationship('User', foreign_keys=[user1_id])
    user2 = relationship('User', foreign_keys=[user2_id])
    messages = relationship('ChatMessage', back_populates='chat', cascade='all, delete-orphan')
    

    # Constraints
    __table_args__ = (
        UniqueConstraint('user1_id', 'user2_id', name='uix_user1_id_user2_id'),
        CheckConstraint('user1_id < user2_id', name='check_user_order'),
    )

class ChatMessage(Base, SerializerMixin):
    __tablename__ = 'ChatMessage'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    sender_id = Column(Integer, ForeignKey('User.id'), nullable=False)  # Foreign key to User
    chat_id = Column(Integer, ForeignKey('PrivateChat.id'), nullable=False)  # Foreign key to PrivateChat
    
    # Relationships
    sender = relationship('User', foreign_keys=[sender_id])
    chat = relationship('PrivateChat', foreign_keys=[chat_id], back_populates='messages')

    @hybrid_property
    def receiver_id(self):
        return self.chat.user2_id if self.sender_id == self.chat.user1_id else self.chat.user1_id

    @hybrid_property
    def receiver(self):
        return self.chat.user2 if self.sender_id == self.chat.user1_id else self.chat.user1

class ChatReadStatus(Base):
    __tablename__ = 'ChatReadStatus'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('PrivateChat.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    is_read = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint('chat_id', 'user_id', name='uix_chat_user_read'),
    )

    chat = relationship('PrivateChat', backref='read_statuses')
    user = relationship('User')
