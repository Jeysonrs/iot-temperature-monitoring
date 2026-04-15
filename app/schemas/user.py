from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    role: str = "operator"


class UserRead(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str | None = None