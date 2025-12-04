from fastapi import APIRouter, HTTPException, status, Request
from database.connection import Database
from models.events import Event, EventUpdate
from typing import List
from internal.state import session_manager

event_router = APIRouter(tags=["Events"])
event_database = Database(Event)

# Вспомогательная функция для получения ID пользователя
def get_current_user_id(request: Request) -> int:
    token = request.cookies.get("access_token")
    user_id = session_manager.get_user_id(token)
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You must sign in first")
    return user_id

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return await event_database.get_all()

@event_router.get("/my", response_model=List[Event])
async def retrieve_my_events(request: Request) -> List[Event]:
    user_id = get_current_user_id(request)
    # Ищем задачи конкретного пользователя
    return await Event.find(Event.creator_id == user_id).to_list()

@event_router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_event(body: Event, request: Request) -> dict:
    user_id = get_current_user_id(request)

    body.id = None
    body.creator_id = user_id
    
    await event_database.save(body)
    return {"message": "Event created", "creator_id": body.creator_id, "event_id": body.id}

@event_router.put("/{id}")
async def update_event(id: int, body: EventUpdate, request: Request) -> Event:
    user_id = get_current_user_id(request)
    
    event = await event_database.get(id)
    if not event:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Event not found")
    
    if event.creator_id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "This is not your event")
    
    updated_event = await event_database.update(id, body)
    return updated_event

@event_router.delete("/{id}")
async def delete_event(id: int, request: Request) -> dict:
    user_id = get_current_user_id(request)
    
    event = await event_database.get(id)
    if not event:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Event not found")
    
    if event.creator_id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "This is not your event")
    
    await event_database.delete(id)
    return {"message": "Event deleted"}
