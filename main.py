import os
from fastapi import FastAPI, Query, Request, Response, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    description="A lightweight in-memory REST API and web dashboard for managing tasks, built with FastAPI and OpenAPI Swagger UI.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount static folder for serving CSS/JS assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initial sample tasks list
INITIAL_TASKS = [
    {"id": 1, "title": "Setup development environment", "done": True},
    {"id": 2, "title": "Build CRUD API endpoints", "done": False},
    {"id": 3, "title": "Test with Swagger UI", "done": False},
]

# In-memory storage
tasks_db = list(INITIAL_TASKS)


# Pydantic Schemas for Swagger Documentation
class TaskSchema(BaseModel):
    id: int = Field(..., example=1, description="Unique identifier for the task")
    title: str = Field(..., example="Buy milk", description="Title or description of the task")
    done: bool = Field(..., example=False, description="Completion status of the task")


class TaskCreateSchema(BaseModel):
    title: str = Field(..., example="Buy milk", description="Title of the new task")


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, example="Buy groceries", description="Updated title")
    done: Optional[bool] = Field(None, example=True, description="Updated completion status")


class StatsSchema(BaseModel):
    total: int = Field(..., example=3, description="Total number of tasks")
    done: int = Field(..., example=1, description="Number of completed tasks")
    open: int = Field(..., example=2, description="Number of pending tasks")


class ErrorSchema(BaseModel):
    error: str = Field(..., example="Task not found", description="Error message explanation")


# Web Dashboard & Favicon & Root Info
@app.get("/", tags=["Dashboard"], summary="Web Dashboard UI")
def read_dashboard():
    """Serves the interactive TaskFlow web dashboard interface."""
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks", "/health", "/stats", "/docs"]}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    """Returns 204 No Content for favicon requests to prevent log noise."""
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/api", tags=["System"], summary="API Overview Info", response_model=dict)
def read_api_info():
    """Returns basic API description, version info, and available endpoint resources."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/health", "/stats", "/docs"]
    }


@app.get("/health", tags=["System"], summary="Health Check", response_model=dict)
def read_health():
    """Health check endpoint used by uptime monitors to verify the server is running."""
    return {"status": "ok"}


@app.get("/tasks", tags=["Tasks"], summary="List All Tasks", response_model=List[TaskSchema])
def get_tasks(
    done: Optional[bool] = Query(None, description="Filter tasks by completion status (true/false)"),
    search: Optional[str] = Query(None, description="Search tasks matching keyword in title")
):
    """Retrieve all tasks from in-memory storage, with optional query filtering by status and search terms."""
    filtered_tasks = tasks_db
    
    if done is not None:
        filtered_tasks = [t for t in filtered_tasks if t["done"] == done]
        
    if search is not None and search.strip():
        keyword = search.strip().lower()
        filtered_tasks = [t for t in filtered_tasks if keyword in t["title"].lower()]
        
    return filtered_tasks


@app.get(
    "/tasks/{task_id}",
    tags=["Tasks"],
    summary="Get Single Task",
    response_model=TaskSchema,
    responses={404: {"model": ErrorSchema, "description": "Task not found"}}
)
def get_task(task_id: int):
    """Retrieve a single task object by its numeric ID. Returns 404 if not found."""
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": f"Task {task_id} not found"}
    )


@app.post(
    "/tasks",
    tags=["Tasks"],
    summary="Create New Task",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskSchema,
    responses={400: {"model": ErrorSchema, "description": "Bad Request / Validation Error"}}
)
async def create_task(request: Request):
    """Create a new task. Requires a JSON payload with a non-empty `title`."""
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


@app.put(
    "/tasks/{task_id}",
    tags=["Tasks"],
    summary="Update Task",
    response_model=TaskSchema,
    responses={
        400: {"model": ErrorSchema, "description": "Validation Error"},
        404: {"model": ErrorSchema, "description": "Task not found"}
    }
)
async def update_task(task_id: int, request: Request):
    """Update an existing task's title and/or done completion status."""
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"}
        )
        
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Invalid or missing JSON payload"}
        )
        
    if not isinstance(data, dict) or not data:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Request body cannot be empty"}
        )
        
    if "title" in data:
        title = data["title"]
        if not isinstance(title, str) or not title.strip():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Title cannot be empty"}
            )
        task["title"] = title.strip()
        
    if "done" in data:
        done = data["done"]
        if not isinstance(done, bool):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Field 'done' must be a boolean"}
            )
        task["done"] = done
        
    return task


@app.delete(
    "/tasks/{task_id}",
    tags=["Tasks"],
    summary="Delete Task",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorSchema, "description": "Task not found"}}
)
def delete_task(task_id: int):
    """Delete a task by ID. Returns HTTP 204 No Content upon success."""
    global tasks_db
    task_idx = next((i for i, t in enumerate(tasks_db) if t["id"] == task_id), None)
    if task_idx is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"}
        )
        
    tasks_db.pop(task_idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Bonus Endpoints
@app.get("/stats", tags=["Extras"], summary="Task Statistics", response_model=StatsSchema)
def get_stats():
    """Retrieve statistical counters for total, completed, and pending tasks."""
    total = len(tasks_db)
    done_count = sum(1 for t in tasks_db if t["done"])
    open_count = total - done_count
    return {
        "total": total,
        "done": done_count,
        "open": open_count
    }


@app.post("/reset", tags=["Extras"], summary="Reset Tasks Database", response_model=dict)
def reset_tasks():
    """Reset the in-memory task database back to the initial 3 sample tasks."""
    global tasks_db
    tasks_db = [dict(t) for t in INITIAL_TASKS]
    return {"message": "Database reset to initial sample tasks", "tasks": tasks_db}
