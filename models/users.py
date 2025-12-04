from typing import Optional, List
from beanie import Document
from pydantic import BaseModel, EmailStr, Field

class User(Document):
    id: Optional[int] = Field(default=None, alias="_id")
    email: EmailStr
    password: str
    events: Optional[List] = []

    class Settings:
        name = "users"

class UserSignIn(BaseModel):
    email: EmailStr
    password: str
