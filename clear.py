from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def clear_database():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.planner
    
    # Удалить ВСЕ коллекции
    await db.events.drop()
    await db.users.drop()      # ← ДОБАВЬТЕ ЭТУ СТРОКУ
    await db.counters.drop()
    
    print("✅ База данных очищена!")
    client.close()

asyncio.run(clear_database())
