from pydantic import BaseModel, Field


class TokenData(BaseModel):
    email: str
    token_version: int = Field(default=0)


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
