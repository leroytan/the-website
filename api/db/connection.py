from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy_utils import database_exists, create_database

DATABASE_USERNAME = "postgres"
DATABASE_PASSWORD = "postgres"
DATABASE_URL = f"""postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost:5432/the"""  # Use SQLite for simplicity
engine = create_engine(DATABASE_URL)

# Create the tables
def init_db():
    if not database_exists(engine.url): create_database(engine.url)
    SQLModel.metadata.create_all(engine)

# Usage example (creating a session)
def get_session():
    with Session(engine) as session:
        yield session

if __name__ == "__main__":
    init_db()
