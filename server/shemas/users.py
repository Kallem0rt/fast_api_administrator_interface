from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """ Проверяет sign-up запрос """
    email: EmailStr
    name: str
    password: str
    superuser: Optional[int]

class UserBase(BaseModel):
    """ Формирует тело ответа с деталями пользователя """
    id: int
    email: EmailStr
    name: str


class TokenBase(BaseModel):
    expires: datetime
    name: str

class User(UserBase):
    """ Формирует тело ответа с деталями пользователя и токеном """
    token: TokenBase = {}
