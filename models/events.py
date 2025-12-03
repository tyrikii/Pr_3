from sqlmodel import JSON, SQLModel, Field, Column
from typing import Optional, List

# Основная модель таблицы
class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    image: str
    description: str
    # SQLModel по умолчанию не умеет хранить списки, используем JSON
    tags: List[str] = Field(sa_column=Column(JSON)) 
    location: str

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event.",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }

# Модель для обновления (все поля необязательные)
class EventUpdate(SQLModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "The launch of the FastAPI book will hold on xyz.",
                "tags": ["python", "fastapi"],
                "location": "virtual"
            }
        }
