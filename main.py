from fastapi import FastAPI, Query, status
from fastapi.responses import JSONResponse
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
