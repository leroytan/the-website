from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables from .env file
load_dotenv(".env")

# Define the settings model
class Settings(BaseSettings):
    is_use_remote: bool = False  # Default to using local DB
    database_url_local: str
    database_url_remote: str
    is_use_mock: bool = True

    # Dynamically determine which database URL to use
    @property
    def database_url(self) -> str:
        if self.use_remote:
            return self.database_url_remote
        return self.database_url_local

# Instantiate the settings object
settings = Settings()

# Now you can access settings like:
# settings.database_url
# settings.use_remote
