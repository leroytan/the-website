from pydantic import BaseModel, Field, EmailStr


class TokenData(BaseModel):
    email: EmailStr
    token_version: int = Field(default=0)


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
