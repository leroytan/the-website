from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy_utils import database_exists, create_database

from api.storage.models import Client, Tutor

DATABASE_USERNAME = "postgres"
DATABASE_PASSWORD = "postgres"
DATABASE_URL = f"""postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost:5432/the"""  # Use SQLite for simplicity
engine = create_engine(DATABASE_URL)

# Create the tables
def init_db():
    if not database_exists(engine.url): create_database(engine.url)
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()

    with Session(engine) as session:

        # Adding a new client
        new_client = Client(email="client@example.com", password_hash="hashed_password", client_specific_field="some_value")
        session.add(new_client)
        session.commit()

        # Adding a new tutor
        new_tutor = Tutor(email="tutor@example.com", password_hash="hashed_password", tutor_specific_field="another_value")
        session.add(new_tutor)
        session.commit()

