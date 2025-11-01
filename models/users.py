from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event

class User(BaseModel):
    email: EmailStr
    password: str
    events: Optional[List[Event]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!",
                "events": []
            }
        }

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
