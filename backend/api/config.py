import os

ENV = os.getenv("APP_ENV")

print(f"Current environment: {ENV}")

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
match ENV:
    case "local":
        load_dotenv(".env.local")
    case "development":
        load_dotenv(".env.development")
    case "test":
        load_dotenv(".env.test")
    case "production":
        load_dotenv(".env.production")
    case _:
        raise ValueError(f"Unknown environment: {ENV}. Please set APP_ENV to 'local', 'development', 'test', or 'production'.")
    

# Define the settings model
class Settings(BaseSettings):
    jwt_algorithm: str = "HS256"
    jwt_secret_key: str
    refresh_token_secret_key: str
    access_token_expire_minutes: int = 30  # Token expiry time
    refresh_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    database_url: str
    is_use_mock: bool = False
    db_populate_check: bool = False
    stripe_api_key: str
    stripe_product_name: str
    stripe_webhook_secret: str
    r2_endpoint: str
    r2_access_key_id: str
    r2_secret_key: str
    r2_bucket_name: str
    r2_bucket_region: str = "auto"  # Default region for R2
    allowed_origins: str = "*"
    gmail_refresh_token: str  # OAuth refresh token for Gmail
    gmail_client_id: str  # OAuth client ID for Gmail
    gmail_client_secret: str  # OAuth client secret for Gmail
    gmail_startup_notification_email: str = ""
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str = "http://localhost:8000/api/auth/google/callback"
    frontend_domain: str = "https://teachhonourexcel.com"

    @property
    def env(self):
        return ENV
    
    @property
    def is_database_local(self):
        return self.database_url.split("@")[-1].startswith("localhost")
            
    def make_engine(self, create_engine: callable, NullPool: callable):
        if self.database_url == "":
            raise ValueError("Database URL is not set. Please check your configuration.")
        if self.is_database_local:
            return create_engine(self.database_url)
        else:
            return create_engine(self.database_url, client_encoding='utf8', poolclass=NullPool)

# Instantiate the settings object
settings = Settings()