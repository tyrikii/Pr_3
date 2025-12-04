from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.users import user_router
from routes.events import event_router
from database.connection import Settings
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код выполняется при запуске
    database = Settings()
    await database.initialize_database()
    yield
    # Код выполняется при остановке (если нужно)

app = FastAPI(lifespan=lifespan)

# Регистрация роутов
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
