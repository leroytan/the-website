from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import ENUM
import enum

# Create a base class for declarative models
Base = declarative_base()

class UserType(enum.Enum):
    """
    Enum for user types
    """
    CLIENT = 'CLIENT'
    TUTOR = 'TUTOR'

class User(Base):
    """
    Base User model with composite primary key of email and userType
    """
    __tablename__ = 'users'

    # Columns
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
    tutor_specific_field = Column(String, nullable=True)

    # Mapper args for inheritance
    __mapper_args__ = {
        "polymorphic_identity": UserType.TUTOR
    }