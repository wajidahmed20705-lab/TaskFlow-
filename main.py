from fastapi import FastAPI, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple task management CRUD API built with FastAPI"
)

# Initial in-memory task database pre-filled with 3 tasks
tasks_db = [
    {"id": 1, "title": "Setup development environment", "done": True},
    {"id": 2, "title": "Build CRUD API endpoints", "done": False},
    {"id": 3, "title": "Test with Swagger UI", "done": False},
]

class TaskCreate(BaseModel):
    title: str = Field(..., description="The title of the task")

@app.get("/")
def read_root():
    """Returns basic API information and available endpoints."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def read_health():
    """Health check endpoint to verify server is operational."""
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks(
    done: Optional[bool] = Query(None, description="Filter tasks by completion status"),
    search: Optional[str] = Query(None, description="Search tasks by title keyword")
):
    """Retrieve all tasks with optional filtering by done status and search keyword."""
    filtered_tasks = tasks_db
    
    if done is not None:
        filtered_tasks = [t for t in filtered_tasks if t["done"] == done]
        
    if search is not None and search.strip():
        keyword = search.strip().lower()
        filtered_tasks = [t for t in filtered_tasks if keyword in t["title"].lower()]
        
    return filtered_tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Retrieve a single task by ID. Returns HTTP 404 if task is not found."""
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": f"Task {task_id} not found"}
    )

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(request: Request):
    """Create a new task. Requires a non-empty title string in JSON body."""
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Invalid or missing JSON payload"}
        )
        
    if not isinstance(data, dict) or "title" not in data:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Title is required"}
        )
        
    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Title cannot be empty"}
        )
        
    next_id = max([t["id"] for t in tasks_db], default=0) + 1
    new_task = {
        "id": next_id,
        "title": title.strip(),
        "done": False
    }
    tasks_db.append(new_task)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_task)
