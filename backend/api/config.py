from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv(".env")

# Define the settings model
class Settings(BaseSettings):
    jwt_algorithm: str = "HS256"
    jwt_secret_key: str
    refresh_token_secret_key: str
    access_token_expire_minutes: int = 30  # Token expiry time
    refresh_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    database_config: str = "LOCAL"  # Default to using local DB
    database_url_local: str
    database_url_dev1: str
    database_url_prod: str
    is_use_mock: bool = True
    db_populate_check: bool = False
    stripe_api_key: str
    r2_endpoint: str
    r2_access_key_id: str
    r2_secret_key: str
    r2_bucket_name: str
    r2_bucket_region: str = "auto"  # Default region for R2
    allowed_origins: str = "*"

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