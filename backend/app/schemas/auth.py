from pydantic import BaseModel, EmailStr
from typing import Literal


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr
    role: Literal["user", "admin"]
    is_verified: bool
    is_banned: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str


class VerifyRequest(BaseModel):
    email: EmailStr
    code: str


class ResendEmailRequest(BaseModel):
    email: EmailStr
