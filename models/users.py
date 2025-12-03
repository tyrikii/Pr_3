from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event

# Модель для базы данных (MongoDB)
class User(Document):
    email: EmailStr
    password: str
    events: Optional[List[Event]] = None

    class Settings:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!",
                "events": []
            }
        }

# Модель для регистрации (Pydantic)
class NewUser(BaseModel):
    email: EmailStr
    password: str
    username: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "username": "FastPackt",
                "password": "strong!!!"
            }
        }

# Модель для входа (Pydantic)
class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!"
            }
        }
