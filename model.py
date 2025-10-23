from typing import List, Optional
from pydantic import BaseModel
from fastapi import Form

class Item(BaseModel):
    item: str
    status: str = "pending"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"item": "Read a book", "status": "pending"}
            ]
        }
    }

class TodoItem(BaseModel):
    item: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"item": "Read the next chapter of the book"}
            ]
        }
    }

class Todo(BaseModel):
    id: Optional[int] = None
    item: Item

    @classmethod
    def as_form(cls, item: str = Form(...), status: str = Form("pending")):
        return cls(item=Item(item=item, status=status))

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"id": 1, "item": {"item": "Learn FastAPI", "status": "pending"}}
            ]
        }
    }

class TodoItems(BaseModel):
    todos: List[TodoItem]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"todos": [{"item": "Learn FastAPI"}, {"item": "Build a project"}]}
            ]
        }
    }
