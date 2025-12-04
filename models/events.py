from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional, List

class Event(Document):
    id: Optional[int] = Field(default=None, alias="_id")
    title: str
    image: str
    description: str
    tags: List[str]
    location: str
    creator_id: Optional[int] = None  # Привязка к пользователю

    class Settings:
        name = "events"

class EventUpdate(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None
