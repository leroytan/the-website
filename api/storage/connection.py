import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_URL = os.getenv("DATABASE_URL").format(DATABASE_NAME = DATABASE_NAME, DATABASE_USERNAME = DATABASE_USERNAME, DATABASE_PASSWORD = DATABASE_PASSWORD)

engine = create_engine(DATABASE_URL)