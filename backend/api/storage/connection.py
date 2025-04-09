from api.config import settings
from sqlalchemy import create_engine

print(f"Database URL: {settings.database_url}")
engine = create_engine(settings.database_url)
