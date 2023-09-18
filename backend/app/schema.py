from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    hashed_password: str

    name: str = ""
    email: str = ""
    roles: List[int] = []
    verified: bool = False
    created_at: Optional[str] = None


class NewUserSchema(BaseModel):
    username: str
    plain_password: str

    roles: List[int] = []

    name: str = ""
    email: str = ""
    verified: bool = False


class LoginResponse(BaseModel):
    user: User
    access_token: str


class RefreshTokenData(BaseModel):
    username: str
    created_at: str
    exp: datetime


class AccessTokenData(BaseModel):
    username: str
    roles: List[int]
    created_at: str
    exp: datetime
