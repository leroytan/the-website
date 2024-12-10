from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from api.storage.connection import engine
from api.storage.storage_interface import StorageInterface
from api.storage.models import Base, User, Client, Tutor, UserType
from api.exceptions import UserAlreadyExistsError, UserNotFoundError, TableEmptyError
from sqlalchemy_utils import database_exists, create_database
from api.common.utils import Utils

class StorageService(StorageInterface):

    @staticmethod
    def init_db():
        # Create the tables if they don't exist
        if not database_exists(engine.url):
            create_database(engine.url)
        # SQLAlchemy automatically creates tables from the Base metadata
        Base.metadata.create_all(engine)
    
    @staticmethod
    def find_one_user(query: dict) -> User:
        # Use SQLAlchemy session for querying
        with Session(engine) as session:
            # Assuming query is a dictionary like {'email': 'user@example.com'}
            statement = select(User).filter_by(**query)
            user = session.execute(statement).scalars().first()  # Use .scalars().first() to get the result
            
        if not user:
            try:
                Utils.validate_non_empty_multiple(query=query)
            except ValueError:
                raise TableEmptyError(User.__tablename__)
            raise UserNotFoundError(email=query.get("email"), userType=query.get("userType"))
        
        return user
    
    @staticmethod
    def create_user(email: str, name: str, password_hash: str, userType: UserType) -> User:
        # Decide which model to use based on userType
        match userType:
            case UserType.CLIENT:
                CurrentUser = Client
            case UserType.TUTOR:
                CurrentUser = Tutor
            case _:
                raise ValueError("Invalid user type")

        # Check if the user already exists based on email and userType
        with Session(engine) as session:
            statement = select(CurrentUser).filter_by(email=email)
            existing_user = session.execute(statement).scalars().first()

            if existing_user:
                raise UserAlreadyExistsError(email, userType)
            
            # Create a new user instance
            new_user = CurrentUser(
                email=email,
                name=name,  # Ensure that `name` is part of the model
                password_hash=password_hash,
                userType=userType  # Assuming userType is an enum
            )

            # Insert the new user into the database
            session.add(new_user)
            try:
                session.commit()  # Commit the transaction
                session.refresh(new_user)  # Get the assigned user ID
            except IntegrityError:
                session.rollback()  # Rollback in case of integrity error (e.g., unique constraint failure)
                raise UserAlreadyExistsError(email, userType)  # Re-raise error for user already existing
        
        return new_user
