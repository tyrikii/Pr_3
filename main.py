from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from database.connection import conn # Импортируем функцию создания БД

from routes.users import user_router
from routes.events import event_router
import uvicorn

app = FastAPI()

# Регистрация маршрутов
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

@app.on_event("startup")
def on_startup():
    conn() # Создаем таблицы при запуске

@app.get("/")
async def home():
    return RedirectResponse(url="/event/")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
