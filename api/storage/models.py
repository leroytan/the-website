from sqlalchemy import Column, ForeignKey, String, Integer, Float, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import ENUM
import enum

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
    id = Column(Integer, unique=True, autoincrement=True, nullable=False)
    email = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    userType = Column(ENUM(UserType), primary_key=True)
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

class Level(Base):
    """
    Level model
    """
    __tablename__ = 'Level'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

# Many-to-many relationship tables

# Define the association tables
TutorSubject = Table('TutorSubject',
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('tutorId', Integer, ForeignKey('Tutor.id')),
    Column('subjectId', Integer, ForeignKey('Subject.id')),
)


TutorLevel = Table('TutorLevel',
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('tutorId', Integer, ForeignKey('Tutor.id')),
    Column('levelId', Integer, ForeignKey('Level.id')),
)


    