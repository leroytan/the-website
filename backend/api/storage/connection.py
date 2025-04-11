from api.config import settings
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

engine = settings.make_engine(create_engine, NullPool)
