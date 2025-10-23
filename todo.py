from typing import List
from fastapi import APIRouter, Path, HTTPException, status, Request, Depends
from fastapi.templating import Jinja2Templates
from model import Todo, TodoItem, TodoItems

todo_router = APIRouter()
todo_list: List[Todo] = []
templates = Jinja2Templates(directory="templates/")

@todo_router.post("/todo")
async def add_todo(request: Request, todo: Todo = Depends(Todo.as_form)):
    todo.id = len(todo_list) + 1
    todo_list.append(todo)
    return templates.TemplateResponse(
        "todo.html",
        {"request": request, "todos": todo_list},
        status_code=status.HTTP_201_CREATED,
    )

@todo_router.get("/todo", response_model=TodoItems)
async def retrieve_todo(request: Request):
    return templates.TemplateResponse(
        "todo.html",
        {"request": request, "todos": todo_list},
    )

@todo_router.get("/todo/{todo_id}")
async def get_single_todo(
    request: Request,
    todo_id: int = Path(..., title="The ID of the todo to retrieve."),
):
    for todo in todo_list:
        if getattr(todo, "id", None) == todo_id:
            return templates.TemplateResponse(
                "todo.html",
                {"request": request, "todo": todo},
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied ID doesn't exist",
    )

@todo_router.put("/todo/{todo_id}")
async def update_todo(
    todo_data: TodoItem,
    todo_id: int = Path(..., title="The ID of the todo to be updated"),
):
    for todo in todo_list:
        if getattr(todo, "id", None) == todo_id:
            todo.item.item = todo_data.item
            return {"message": "Todo updated successfully."}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with this ID doesn't exist.",
    )

@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(
    todo_id: int = Path(..., title="The ID of the todo to delete")
):
    for todo in list(todo_list):
        if getattr(todo, "id", None) == todo_id:
            todo_list.remove(todo)
            return {"message": "Todo deleted successfully."}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied ID doesn't exist.",
    )

@todo_router.delete("/todo")
async def delete_all_todo():
    todo_list.clear()
    return {"message": "Todos deleted successfully."}
