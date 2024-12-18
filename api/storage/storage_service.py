from typing import Optional, Type
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from api.storage.connection import engine
from api.storage.storage_interface import StorageInterface
from api.storage.models import Base, User, Client, Tutor, UserType, TutorSubject, Subject
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
    def find_one_tutor(query: dict) -> Tutor:
        return StorageService.find_one_user(query, Tutor)

    @staticmethod
    def find_one_client(query: dict) -> Client:
        return StorageService.find_one_user(query, Client)

    @staticmethod
    def find_one_user(query: dict, TableClass: Optional[Type[User]] = User) -> User:
        return StorageService.find_users(query, TableClass, find_one=True)

    @staticmethod
    def find_many_tutors(query: dict) -> list[Tutor]:
        return StorageService.find_many_users(query, Tutor)

    @staticmethod
    def find_many_clients(query: dict) -> list[Client]:
        return StorageService.find_many_users(query, Client)

    @staticmethod
    def find_many_users(query: dict, TableClass: Optional[Type[User]] = User) -> list[User]:
        return StorageService.find_users(query, TableClass, find_one=False)

    @staticmethod
    def find_users(query: dict, TableClass: Optional[Type[User]] = User, find_one: bool = False) -> list[User]:
        # Use SQLAlchemy session for querying
        with Session(engine) as session:
            statement = select(TableClass).filter_by(**query)
            res = session.execute(statement).scalars()
            if find_one:
                user = res.first()  # Use .first() to get the result
            else:
                user = res.all()

        if not user:
            try:
                Utils.validate_non_empty(query=query)
            except ValueError:
                # query is empty
                raise TableEmptyError(TableClass.__tablename__)
            raise UserNotFoundError(query=query, TableClass=TableClass)

        return user

    @staticmethod
    def get_tutor_summaries() -> dict:
        with Session(engine) as session:
            statement = select(Tutor).join(TutorSubject).join(Subject).options(
                # Ensuring subjects are loaded correctly
                joinedload(Tutor.subjects)
            ).with_only_columns(
                Tutor.id,
                Tutor.name,
                Tutor.photoUrl,
                Tutor.rate,
                Tutor.rating,
                Tutor.subjects,
                Tutor.experience,
                Tutor.availability,
            )
            tutors = session.execute(statement).scalars().all()

        return tutors

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
                password_hash=password_hash
            )

            # Insert the new user into the database
            session.add(new_user)
            try:
                session.commit()  # Commit the transaction
                session.refresh(new_user)  # Get the assigned user ID
            except IntegrityError as e:
                print(f"IntegrityError: User with email {email} already exists")
                print(e)
                session.rollback()  # Rollback in case of integrity error (e.g., unique constraint failure)
                # Re-raise error for user already existing
                raise UserAlreadyExistsError(email, userType)

        return new_user
