import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt
from typing import Optional

from api.auth.auth_interface import AuthInterface
from api.auth.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from api.common.utils import Utils

class AuthService(AuthInterface):

    @staticmethod
    def hash_password(password: str) -> str:
        Utils.validate_non_empty_multiple(password = password)
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        Utils.validate_non_empty_multiple(plain_password = plain_password, hashed_password = hashed_password)
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        Utils.validate_non_empty_multiple(data = data)
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def verify_token(token: str):
        Utils.validate_non_empty_multiple(token = token)
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload