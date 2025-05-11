from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv(".env")

# Define the settings model
class Settings(BaseSettings):
    database_config: str = "LOCAL"  # Default to using local DB
    database_url_local: str
    database_url_dev1: str
    database_url_prod: str
    is_use_mock: bool = True
    db_populate_check: bool = False
    stripe_api_key: str

    # Dynamically determine which database URL to use
    @property
    def database_url(self) -> str:
        print("Using database config:", self.database_config)
        match self.database_config:
            case "LOCAL":
                return self.database_url_local
            case "DEV1":
                return self.database_url_dev1
            case "PROD":
                return self.database_url_prod
            
    def make_engine(self, create_engine: callable, NullPool: callable):
        if self.database_config == "LOCAL":
            return create_engine(self.database_url)
        else:
            return create_engine(self.database_url, client_encoding='utf8', poolclass=NullPool)

# Instantiate the settings object
settings = Settings()