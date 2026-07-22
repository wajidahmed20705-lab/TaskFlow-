from fastapi import FastAPI

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple task management CRUD API built with FastAPI"
)

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
