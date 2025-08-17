from sqlalchemy import create_engine

from api.config import settings

engine = settings.make_engine(create_engine)
