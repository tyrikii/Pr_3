from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Any, List
from pydantic_settings import BaseSettings
from pydantic import BaseModel

from models.events import Event
from models.users import User

# Модель для счетчика ID
class Counter(Document):
    id: str
    sequence_value: int
    class Settings:
        name = "counters"

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(
            database=client.get_default_database(),
            document_models=[Event, User, Counter]
        )

    class Config:
        env_file = ".env"

class Database:
    def __init__(self, model):
        self.model = model

    async def get_next_id(self, counter_name: str) -> int:
        counter = await Counter.find_one(Counter.id == counter_name)
        if not counter:
            counter = Counter(id=counter_name, sequence_value=1)
            await counter.insert()
            return 1
        else:
            counter.sequence_value += 1
            await counter.save()
            return counter.sequence_value

    async def save(self, document) -> None:
        # Если ID нет, создаем новый числовой
        if hasattr(document, 'id') and document.id is None:
            model_name = self.model.__name__.lower()
            document.id = await self.get_next_id(f"{model_name}_id")
        await document.insert()

    async def get(self, id: int) -> Any:
        return await self.model.find_one(self.model.id == id)

    async def get_all(self) -> List[Any]:
        return await self.model.find_all().to_list()

    async def update(self, id: int, body: BaseModel) -> Any:
        doc = await self.get(id)
        if not doc: return False
        
        des_body = body.dict(exclude_unset=True)
        des_body = {k: v for k, v in des_body.items() if v is not None}
        
        await doc.update({"$set": des_body})
        return doc

    async def delete(self, id: int) -> bool:
        doc = await self.get(id)
        if not doc: return False
        await doc.delete()
        return True
