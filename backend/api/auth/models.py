from pydantic import BaseModel


class TokenData(BaseModel):
    email: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str