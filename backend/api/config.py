from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv(".env")

# Define the settings model
class Settings(BaseSettings):
    is_use_remote: bool = False  # Default to using local DB
    database_url_local: str
    database_url_remote: str
    is_use_mock: bool = True
    db_populate_check: bool = False

    # Dynamically determine which database URL to use
    @property
    def database_url(self) -> str:
        if self.is_use_remote:
            return self.database_url_remote
        return self.database_url_local

# Instantiate the settings object
settings = Settings()