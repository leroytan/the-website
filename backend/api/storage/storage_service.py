from typing import Type

from api.config import settings
from api.exceptions import TableEmptyError, UserAlreadyExistsError
from api.storage.connection import engine as default_engine
from api.storage.models import Base, User
from api.storage.populate import insert_test_data
from api.storage.storage_interface import StorageInterface
# from api.storage.validate import check_data
from sqlalchemy import ColumnElement, Engine, and_, or_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy_utils import create_database, database_exists


class StorageService(StorageInterface):

    engine: Engine = None

    @staticmethod
    def init_db(db_engine=default_engine):
        print("Initializing database")
        # Create the tables if they don't exist
        if not database_exists(db_engine.url):
            print("Creating database")
            create_database(db_engine.url)
            print("Database created")
            # SQLAlchemy automatically creates tables from the Base metadata
            Base.metadata.create_all(db_engine)
            print("Tables created")
            if settings.db_populate_check:
                print("Inserting test data")
                insert_test_data(db_engine)
                # check_data(db_engine)
                print("Test data inserted")
        StorageService.engine = db_engine
        print("Database initialized")
    
    @staticmethod
    def find(session: Session, query: dict | list[ColumnElement], TableClass: Type[DeclarativeMeta], find_one: bool = False) -> list[DeclarativeMeta] | DeclarativeMeta:
        from api.common.utils import Utils

        with Session(StorageService.engine) as session:
            statement = select(TableClass)
            if isinstance(query, list):
                for q in query:
                    statement = statement.where(q)
            elif isinstance(query, dict):
                statement = statement.filter_by(**query)
            else:
                raise ValueError("Query must be a dictionary or a list of ColumnElement objects.")
            
            # Execute the query
            res = session.execute(statement).scalars()
            result = res.first() if find_one else res.all()

        if not result:
            try:
                Utils.validate_non_empty(query=query)
            except ValueError:
                # query is empty
                raise TableEmptyError(TableClass.__tablename__)
            
        return result
    
    @staticmethod
    def find_any(session: Session, queries: list[dict], TableClass: Type[DeclarativeMeta], find_one: bool = False) -> list[DeclarativeMeta] | DeclarativeMeta:
        from api.common.utils import Utils

        with Session(StorageService.engine) as session:
            # Build OR conditions
            conditions = [and_(*[getattr(TableClass, key) == value for key, value in query.items()]) for query in queries]
            statement = select(TableClass).where(or_(*conditions))
            
            res = session.execute(statement).scalars()
            result = res.first() if find_one else res.all()

        if not result:
            try:
                Utils.validate_non_empty(query=queries)
            except ValueError:
                raise TableEmptyError(TableClass.__tablename__)

        return result
    
    @staticmethod
    def update(session: Session, query: dict | list[ColumnElement], values: dict, TableClass: Type[DeclarativeMeta]) -> DeclarativeMeta:
        
        statement = update(TableClass).where(and_(*[getattr(TableClass, key) == value for key, value in query.items()])).values(**values)
        session.execute(statement)
        session.commit()
        return StorageService.find(session, query, TableClass, find_one=True)
    
    @staticmethod
    def insert(session: Session, obj: DeclarativeMeta) -> DeclarativeMeta:
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj
    
    @staticmethod
    def create_user(session: Session, user: User):
        """
        Add a new user to the database.
        """
        with Session(StorageService.engine) as session:
            try:
                session.add(user)
                session.commit()
                session.refresh(user)  # Get the assigned user ID
            except IntegrityError as e:
                print(f"IntegrityError: User with email {user.email} already exists")
                print(e)
                session.rollback()  # Rollback in case of integrity error (e.g., unique constraint failure)
                # Re-raise error for user already existing
                raise UserAlreadyExistsError(user.email, User)    
