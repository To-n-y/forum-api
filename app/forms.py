from pydantic import BaseModel
from typing import Optional


class UserLoginForm(BaseModel):
    email: str
    password: str


class UserCreateForm(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    surname: Optional[str] = None


class MessageCreateForm(BaseModel):
    text: str
