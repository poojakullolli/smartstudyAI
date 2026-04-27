from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import List, Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserDisplay(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

