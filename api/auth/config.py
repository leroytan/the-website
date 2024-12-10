# config.py
import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key_here")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiry time
REFRESH_TOKEN_SECRET_KEY = os.getenv("REFRESH_TOKEN_SECRET_KEY", "your_refresh_secret_key_here")
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days