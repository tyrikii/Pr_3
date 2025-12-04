from fastapi import APIRouter, HTTPException, Response, Request, status, Depends
from database.connection import Database
from models.users import User, UserSignIn
from models.events import Event
from internal.state import session_manager

user_router = APIRouter(tags=["User"])
user_database = Database(User)

@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_user_up(user: User) -> dict:
    # Проверяем, существует ли пользователь
    if await User.find_one(User.email == user.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "User with this email already exists")
    
    # Создаем пользователя (ID генерируется автоматически в database.save)
    user.id = None 
    await user_database.save(user)
    return {"message": "User created successfully"}

@user_router.post("/signin")
async def sign_user_in(user: UserSignIn, response: Response) -> dict:
    db_user = await User.find_one(User.email == user.email)
    
    if not db_user or db_user.password != user.password:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Wrong credentials")
    
    # Генерируем токен и сохраняем его
    token = session_manager.create_session(db_user.id)
    
    # Устанавливаем куку (HttpOnly для безопасности)
    response.set_cookie(key="access_token", value=token, httponly=True)
    
    return {"message": f"Welcome back! You are logged in as ID {db_user.id}"}

@user_router.post("/signout")
async def sign_out(request: Request, response: Response) -> dict:
    token = request.cookies.get("access_token")
    if token:
        session_manager.remove_session(token)
    
    response.delete_cookie("access_token")
    return {"message": "Signed out successfully"}

@user_router.delete("/me")
async def delete_me(request: Request, response: Response) -> dict:
    """
    Удаляет текущего пользователя и все его события.
    """
    token = request.cookies.get("access_token")
    user_id = session_manager.get_user_id(token)
    
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You must sign in first")

    # 1. Удаляем все события пользователя
    await Event.find(Event.creator_id == user_id).delete()
    
    # 2. Удаляем самого пользователя
    deleted = await user_database.delete(user_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found in DB")
    
    # 3. Очищаем сессию
    session_manager.remove_session(token)
    response.delete_cookie("access_token")
    
    return {"message": "User and all related events deleted successfully"}
