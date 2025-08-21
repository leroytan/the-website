import enum

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin

# Create a base class for declarative models
Decl_Base = declarative_base()


class Base(Decl_Base):
    __abstract__ = True
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class SortableMixin:
    @declared_attr
    def sort_order(cls):
        return Column(Integer, nullable=False)


class EmailVerificationStatus(enum.Enum):
    """
    Enum for email verification status
    """

    VERIFIED = "verified"
    PENDING = "pending"
    WAITLISTED = "waitlisted"


class User(Base, SerializerMixin):
    """Base User model"""

    __tablename__ = "User"

    # Core user fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(
        String, nullable=True
    )  # Made nullable for Google-only accounts
    google_id = Column(
        String, unique=True, index=True, nullable=True
    )  # New field for Google ID
    token_version = Column(Integer, default=0)
    intends_to_be_tutor = Column(Boolean, default=False)

    # Email confirmation fields
    email_verification_status = Column(
        ENUM(EmailVerificationStatus), default=EmailVerificationStatus.PENDING
    )
    email_confirmation_token = Column(String, nullable=True)
    email_confirmation_token_expires_at = Column(DateTime(timezone=True), nullable=True)

    # Password reset fields
    password_reset_token = Column(String, nullable=True)
    password_reset_token_expires_at = Column(DateTime(timezone=True), nullable=True)

    tutor_role = relationship("Tutor", back_populates="user", uselist=False)
    
    def to_dict(self):
        """Override to_dict to exclude sensitive fields"""
        data = super().to_dict()
        # Remove sensitive fields
        sensitive_fields = [
            'password_hash', 
            'password_reset_token', 
            'password_reset_token_expires_at', 
            'email_confirmation_token', 
            'email_confirmation_token_expires_at'
        ]
        for field in sensitive_fields:
            data.pop(field, None)
        return data


# TODO: Decide which fields in tutor are required and which are optional
class Tutor(Base):
    """Tutor-specific role model"""

    __tablename__ = "Tutor"

    id = Column(Integer, ForeignKey("User.id"), primary_key=True)

    # Tutor-specific fields
    highest_education = Column(String, nullable=True)
    availability = Column(String, nullable=True)
    resume_url = Column(String, nullable=True)
    min_rate = Column(Integer, nullable=True)
    max_rate = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    about_me = Column(String, nullable=True)
    experience = Column(String, nullable=True)

    # Relationships
    subjects = relationship(
        "Subject", secondary="TutorSubject", back_populates="tutors"
    )
    levels = relationship("Level", secondary="TutorLevel", back_populates="tutors")
    special_skills = relationship(
        "SpecialSkill", secondary="TutorSpecialSkill", back_populates="tutors"
    )
    user = relationship("User", back_populates="tutor_role")


class AssignmentStatus(enum.Enum):
    """
    Enum for assignment status
    """

    OPEN = "OPEN"
    FILLED = "FILLED"


class Assignment(Base, SerializerMixin):
    """
    Assignment model
    """

    __tablename__ = "Assignment"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("User.id"))  # Foreign key to User
    tutor_id = Column(
        Integer, ForeignKey("Tutor.id"), nullable=True
    )  # Foreign key to Tutor
    level_id = Column(
        Integer, ForeignKey("Level.id"), nullable=False
    )  # Foreign key to Level
    estimated_rate_hourly = Column(Integer, nullable=False)
    lesson_duration = Column(Integer, nullable=False)  # Duration in minutes
    weekly_frequency = Column(Integer, nullable=False)
    special_requests = Column(String, nullable=True)
    location_id = Column(
        Integer, ForeignKey("Location.id"), nullable=False
    )  # Foreign key to Location
    status = Column(ENUM(AssignmentStatus), default=AssignmentStatus.OPEN)

    # Relationships
    owner = relationship("User", foreign_keys=[owner_id])
    tutor = relationship("Tutor", foreign_keys=[tutor_id])
    subjects = relationship(
        "Subject", secondary="AssignmentSubject", back_populates="assignments"
    )
    level = relationship("Level", foreign_keys=[level_id], back_populates="assignments")
    location = relationship(
        "Location", foreign_keys=[location_id], back_populates="assignments"
    )
    assignment_requests = relationship("AssignmentRequest", back_populates="assignment")
    available_slots = relationship(
        "AssignmentSlot",
        back_populates="assignment",
        primaryjoin="Assignment.id == AssignmentSlot.assignment_id",
    )


class AssignmentSlot(Base):
    """
    Assignment Slot model
    """

    __tablename__ = "AssignmentSlot"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    assignment_id = Column(
        Integer, ForeignKey("Assignment.id"), nullable=True
    )  # Foreign key to Assignment
    assignment = relationship("Assignment", back_populates="available_slots")
    assignment_request_id = Column(
        Integer, ForeignKey("AssignmentRequest.id"), nullable=True
    )  # Foreign key to Assignment
    assignment_request = relationship(
        "AssignmentRequest", back_populates="available_slots"
    )
    day = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)


class AssignmentRequestStatus(enum.Enum):
    """
    Enum for assignment request status
    """

    NOT_SUBMITTED = "NOT_SUBMITTED"
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class AssignmentRequest(Base):
    """
    Assignment Request model
    """

    __tablename__ = "AssignmentRequest"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    assignment_id = Column(
        Integer, ForeignKey("Assignment.id")
    )  # Foreign key to Assignment
    tutor_id = Column(Integer, ForeignKey("Tutor.id"))  # Foreign key to Tutor
    requested_rate_hourly = Column(Integer, nullable=False)
    requested_duration = Column(Integer, nullable=False)  # Duration in minutes
    status = Column(
        ENUM(AssignmentRequestStatus), default=AssignmentRequestStatus.PENDING
    )
    chat_message_id = Column(
        Integer, ForeignKey("ChatMessage.id"), nullable=True
    )  # Foreign key to ChatMessage

    # Relationships
    tutor = relationship("Tutor", foreign_keys=[tutor_id])
    assignment = relationship(
        "Assignment", foreign_keys=[assignment_id], back_populates="assignment_requests"
    )
    available_slots = relationship(
        "AssignmentSlot",
        back_populates="assignment_request",
        cascade="all, delete-orphan",
    )
    chat_message = relationship(
        "ChatMessage", foreign_keys=[chat_message_id], uselist=False
    )

    # Constraints
    # Composite unique constraint on column1 and column2
    __table_args__ = (
        UniqueConstraint(
            "assignment_id", "tutor_id", name="uix_assignment_id_tutor_id"
        ),
    )


class SpecialSkill(Base):
    """
    SpecialSkill model
    """

    __tablename__ = "SpecialSkill"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    tutors = relationship(
        "Tutor", secondary="TutorSpecialSkill", back_populates="special_skills"
    )

    @hybrid_property
    def filter_id(self):
        return f"special_skill_{self.name.lower().replace(' ', '_')}"

    @filter_id.expression
    def filter_id(cls):
        # This is used in SQL queries (e.g. SpecialSkill.filter_id == ...)
        return func.concat(
            "special_skill_", func.replace(func.lower(cls.name), " ", "_")
        )


class TutorSpecialSkill(Base):
    __tablename__ = "TutorSpecialSkill"

    id = Column(Integer, primary_key=True)
    tutor_id = Column(Integer, ForeignKey("Tutor.id"))
    special_skill_id = Column(Integer, ForeignKey("SpecialSkill.id"))


class Subject(Base):
    """
    Subject model
    """

    __tablename__ = "Subject"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    tutors = relationship("Tutor", secondary="TutorSubject", back_populates="subjects")
    assignments = relationship(
        "Assignment", secondary="AssignmentSubject", back_populates="subjects"
    )

    @hybrid_property
    def filter_id(self):
        return f"subject_{self.name.lower().replace(' ', '_')}"

    @filter_id.expression
    def filter_id(cls):
        # This is used in SQL queries (e.g. Subject.filter_id == ...)
        return func.concat("subject_", func.replace(func.lower(cls.name), " ", "_"))


class TutorSubject(Base):
    __tablename__ = "TutorSubject"

    id = Column(Integer, primary_key=True)
    tutor_id = Column(Integer, ForeignKey("Tutor.id"))
    subjectId = Column(Integer, ForeignKey("Subject.id"))


class AssignmentSubject(Base):
    __tablename__ = "AssignmentSubject"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("Assignment.id"))
    subjectId = Column(Integer, ForeignKey("Subject.id"))


class Level(Base, SortableMixin):
    """
    Level model
    """

    __tablename__ = "Level"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    tutors = relationship("Tutor", secondary="TutorLevel", back_populates="levels")
    assignments = relationship("Assignment", back_populates="level")

    @hybrid_property
    def filter_id(self):
        return f"level_{self.name.lower().replace(' ', '_')}"

    @filter_id.expression
    def filter_id(cls):
        # This is used in SQL queries (e.g. Level.filter_id == ...)
        return func.concat("level_", func.replace(func.lower(cls.name), " ", "_"))


class TutorLevel(Base):
    __tablename__ = "TutorLevel"

    id = Column(Integer, primary_key=True)
    tutor_id = Column(Integer, ForeignKey("Tutor.id"))
    level_id = Column(Integer, ForeignKey("Level.id"))


class Location(Base):
    """
    Location model
    """

    __tablename__ = "Location"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    assignments = relationship("Assignment", back_populates="location")

    @hybrid_property
    def filter_id(self):
        return f"location_{self.name.lower().replace(' ', '_')}"

    @filter_id.expression
    def filter_id(cls):
        # This is used in SQL queries (e.g. Location.filter_id == ...)
        return func.concat("location_", func.replace(func.lower(cls.name), " ", "_"))


class PrivateChat(Base, SerializerMixin):
    __tablename__ = "PrivateChat"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    user1_id = Column(
        Integer, ForeignKey("User.id"), nullable=False
    )  # Foreign key to User
    user2_id = Column(
        Integer, ForeignKey("User.id"), nullable=False
    )  # Foreign key to User
    is_locked = Column(Boolean, default=True)

    # TODO: Implement alias names for locked chats
    # user_1_alias = Column(String, nullable=True)
    # user_2_alias = Column(String, nullable=True)

    # Relationships
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])
    messages = relationship(
        "ChatMessage", back_populates="chat", cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="uix_user1_id_user2_id"),
        CheckConstraint("user1_id < user2_id", name="check_user_order"),
    )


class ChatMessageType(enum.Enum):
    """
    Enum for chat message types
    """

    TEXT_MESSAGE = "text_message"
    TUTOR_REQUEST = "tutor_request"


class TutorRequestStatus(enum.Enum):
    """
    Enum for tutor request status
    """

    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    EXPIRED = "EXPIRED"


class ChatMessage(Base, SerializerMixin):
    __tablename__ = "ChatMessage"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    filtered_content = Column(String, nullable=True)
    is_flagged = Column(Boolean, default=False)
    message_type = Column(
        ENUM(ChatMessageType), nullable=False, default=ChatMessageType.TEXT_MESSAGE
    )
    sender_id = Column(
        Integer, ForeignKey("User.id"), nullable=False
    )  # Foreign key to User
    chat_id = Column(
        Integer, ForeignKey("PrivateChat.id"), nullable=False
    )  # Foreign key to PrivateChat
    assignment_request = relationship(
        "AssignmentRequest", back_populates="chat_message", uselist=False
    )

    # Relationships
    sender = relationship("User", foreign_keys=[sender_id])
    chat = relationship(
        "PrivateChat", foreign_keys=[chat_id], back_populates="messages"
    )

    def receiver_id_from_chat(self, chat: PrivateChat) -> int:
        return chat.user2_id if self.sender_id == chat.user1_id else chat.user1_id

    @hybrid_property
    def receiver_id(self):
        return self.receiver_id_from_chat(self.chat)

    @hybrid_property
    def receiver(self):
        return (
            self.chat.user2 if self.sender_id == self.chat.user1_id else self.chat.user1
        )


class ChatReadStatus(Base):
    __tablename__ = "ChatReadStatus"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("PrivateChat.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    is_read = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint("chat_id", "user_id", name="uix_chat_user_read"),
    )

    chat = relationship("PrivateChat", backref="read_statuses")
    user = relationship("User")


class ChatNotificationTracker(Base):
    """
    Tracks notification status for private chats
    Implements async chat notification strategy
    """

    __tablename__ = "ChatNotificationTracker"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("PrivateChat.id"), nullable=False)
    notification_count = Column(Integer, default=0, nullable=False)
    last_notification_timestamp = Column(DateTime(timezone=True), nullable=True)

    # Relationship to PrivateChat
    chat = relationship("PrivateChat", backref="notification_tracker")

    __table_args__ = (
        UniqueConstraint("chat_id", name="uix_chat_notification_tracker"),
    )
