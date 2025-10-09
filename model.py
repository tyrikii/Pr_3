from pydantic import BaseModel

class Item(BaseModel):
    item: str
    status: str

class Todo(BaseModel):
    id: int
    item: Item

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "item": {
                        "item": "Example schema!",
                        "status": "pending"
                    }
                }
            ]
        }
    }
