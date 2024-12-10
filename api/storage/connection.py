from sqlalchemy import create_engine

DATABASE_USERNAME = "postgres"
DATABASE_PASSWORD = "postgres"
DATABASE_URL = f"""postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost:5432/the"""  # Use SQLite for simplicity
engine = create_engine(DATABASE_URL)