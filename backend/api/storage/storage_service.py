from typing import Type

from api.config import settings
from api.exceptions import TableEmptyError
from api.storage.connection import engine as default_engine
from api.storage.models import Base
from api.storage.populate import insert_test_data
# from api.storage.validate import check_data
from sqlalchemy import (ColumnElement, Engine, and_, inspect, or_, select,
                        update)
from sqlalchemy.orm import Query, Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy_utils import create_database, database_exists


class StorageService:

    engine: Engine = None

    @staticmethod
    def init_db(db_engine=default_engine):
        print("Initializing database")
        exists = database_exists(db_engine.url)
        if not exists or not inspect(db_engine).get_table_names():
            if not exists:
                print("Creating database")
                create_database(db_engine.url)
                print("Database created")
            # SQLAlchemy automatically creates tables from the Base metadata
            Base.metadata.create_all(db_engine)
            print("Tables created")
            if settings.db_populate_check:
                print("Inserting test data")
                success = insert_test_data(db_engine)
                # check_data(db_engine)
                print("Test data inserted")
        StorageService.engine = db_engine
        print("Database initialized")
    
    @staticmethod
    def find(session: Session, query: dict | list[ColumnElement] | Query, TableClass: Type[DeclarativeMeta], find_one: bool = False) -> list[DeclarativeMeta] | DeclarativeMeta:
        from api.common.utils import Utils

        with Session(StorageService.engine) as session:
            statement = select(TableClass)
            if isinstance(query, Query):
                statement = query
            elif isinstance(query, list):
                statement = statement.where(and_(*query))
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