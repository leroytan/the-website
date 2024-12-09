
from api.storage.connection import engine
from api.storage.storage_interface import StorageInterface
from api.storage.models import Client
from api.storage.models import Tutor

from api.exceptions import UserAlreadyExistsError
from api.exceptions import UserNotFoundError

from sqlmodel import Session, select

class StorageService(StorageInterface):
    
    @classmethod
    def find_one_user(cls, query: dict) -> Client:
        with Session(engine) as session:
            statement = select(Client).where(**query)
            user = session.exec(statement).first()
        
        if not user:
            raise UserNotFoundError
        
        return user
    
    @classmethod
    def create_user(cls, email: str, name: str, password_hash: str, userType: str) -> Client:
        
        # Decide which model to use
        if userType == "client":
            CurrentUser = Client
        elif userType == "tutor":
            CurrentUser = Tutor
        else:
            raise ValueError("Invalid user type")
        
        # Check if the user already exists based on email and user type
        with Session(engine) as session:
            statement = select(CurrentUser).where(CurrentUser.email == email)
            existing_user = session.exec(statement).first()

            if existing_user:
                raise UserAlreadyExistsError(email)
            
        # Create a new user
        new_user = CurrentUser(
            email=email,
            name=name,
            password_hash=password_hash
        )

        # Insert the user into the database
        with Session(engine) as session:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)  # Get the assigned user ID

        return new_user
