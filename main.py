from fastapi import FastAPI
from routes.users import user_router
from routes.events import event_router
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.events import Event
from models.users import User
import uvicorn

app = FastAPI()

# Регистрация роутов
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

@app.on_event("startup")
async def on_startup():
    # Подключение к локальной MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    # Инициализация базы "planner"
    await init_beanie(database=client.planner, document_models=[Event, User])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
