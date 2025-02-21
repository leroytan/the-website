from api.config import settings
from sqlalchemy import create_engine

engine = create_engine(settings.database_url)
