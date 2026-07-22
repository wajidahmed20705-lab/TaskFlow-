from fastapi import FastAPI

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple task management CRUD API built with FastAPI"
)

@app.get("/")
def read_root():
    return {"message": "Hello, server!"}
