# FlyRank Backend Track - Week 2 (Assignment A1): Build Your First CRUD API

A clean, production-structured RESTful To-Do CRUD API built with **Python 3.14**, **FastAPI**, and **Uvicorn**, featuring interactive **Swagger UI** documentation (`/docs`) and in-memory state management.

---

## 🚀 Quick Start (One Command)

Clone the repository, create a virtual environment, install dependencies, and start the server:

```bash
git clone https://github.com/your-username/flyrank-crud-api.git
cd flyrank-crud-api
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be live at `http://localhost:8000`.

---

## 📌 API Endpoints Reference

| Method | Endpoint | Description | Expected Status Codes |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Root endpoint displaying API name, version & endpoints | `200 OK` |
| `GET` | `/health` | Health check endpoint returning status | `200 OK` |
| `GET` | `/tasks` | List all tasks (supports `?done=true` & `?search=kw`) | `200 OK` |
| `GET` | `/tasks/{id}` | Retrieve a single task by ID | `200 OK`, `404 Not Found` |
| `POST` | `/tasks` | Create a new task (body: `{"title": "..."}`) | `201 Created`, `400 Bad Request` |
| `PUT` | `/tasks/{id}` | Update task title and/or done status | `200 OK`, `400 Bad Request`, `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Delete task by ID | `204 No Content`, `404 Not Found` |
| `GET` | `/stats` | Statistics summary (`total`, `done`, `open`) | `200 OK` |
| `POST` | `/reset` | Reset database back to initial 3 sample tasks | `200 OK` |

---

## 🧪 Sample `curl -i` Verification Outputs

### 1. Read All Tasks (`GET /tasks`)
```http
HTTP/1.1 200 OK
date: Wed, 22 Jul 2026 22:04:19 GMT
server: uvicorn
content-length: 172
content-type: application/json

[
  {"id":1,"title":"Setup development environment","done":true},
  {"id":2,"title":"Build CRUD API endpoints","done":false},
  {"id":3,"title":"Test with Swagger UI","done":false}
]
```

### 2. Create Task with Validation (`POST /tasks`)
```http
HTTP/1.1 201 Created
date: Wed, 22 Jul 2026 22:05:32 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

```http
HTTP/1.1 400 Bad Request
date: Wed, 22 Jul 2026 22:05:32 GMT
server: uvicorn
content-length: 33
content-type: application/json

{"error":"Title cannot be empty"}
```

### 3. Update Task (`PUT /tasks/2`)
```http
HTTP/1.1 200 OK
date: Wed, 22 Jul 2026 22:06:50 GMT
server: uvicorn
content-length: 55
content-type: application/json

{"id":2,"title":"Build CRUD API endpoints","done":true}
```

### 4. Delete Task (`DELETE /tasks/3`)
```http
HTTP/1.1 204 No Content
date: Wed, 22 Jul 2026 22:06:50 GMT
server: uvicorn
```

### 5. Unknown Resource handling (`GET /tasks/99`)
```http
HTTP/1.1 404 Not Found
date: Wed, 22 Jul 2026 22:04:20 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"error":"Task 99 not found"}
```

---

## 📖 Swagger UI Interactive Documentation

FastAPI automatically generates interactive OpenAPI documentation.

Visit **`http://localhost:8000/docs`** in your browser to view the interactive Swagger UI interface. You can click **"Try it out"** on any endpoint to test all CRUD requests directly from your web browser without typing `curl` commands.

---

## 💡 The Mortality Experiment

When new tasks were created or modified and the FastAPI server process was restarted, all newly created tasks disappeared and the list reverted back to the initial 3 sample tasks. 
This occurs because task data is stored purely in an **in-memory Python list (`tasks_db`)** rather than a persistent database. Once the process terminates, its RAM memory state is discarded.

---

## 🥊 Stage 7: AI vs Me

### Prompt Used
> "Build a Python FastAPI REST API that manages an in-memory to-do list. Include endpoints for GET /, GET /health, GET /tasks, GET /tasks/{id}, POST /tasks, PUT /tasks/{id}, and DELETE /tasks/{id}. Ensure correct HTTP status codes (200, 201, 204, 400, 404), return json error messages when title is missing or empty, auto-increment IDs, and support built-in Swagger UI at /docs."

### Key Differences Found

1. **Error Response Key Formatting**:
   - **AI Generation**: Returned default FastAPI Pydantic validation errors structured as `{"detail": [...]}`.
   - **Hand-built API**: Explicitly mapped custom JSON error responses to `{"error": "Task 99 not found"}` matching the exact spec requirements.

2. **Validation Rigor**:
   - **AI Generation**: Checked if `title` string existed, but allowed whitespace-only strings (e.g. `"   "`).
   - **Hand-built API**: Trimmed strings (`title.strip()`) and returned `400 Bad Request` if whitespace-only.

3. **Status Code Precision**:
   - **AI Generation**: Returned `200 OK` with `{"message": "deleted"}` on `DELETE /tasks/{id}` instead of HTTP `204 No Content`.
   - **Hand-built API**: Used exact REST standards (`204 No Content` with an empty response body).

---

## 📜 Commit History

- `ed745e5` Stage 0: hello server
- `17812b3` Stage 1: root and health endpoints
- `6deea2c` Stage 2: read endpoints with 404
- `99bf74f` Stage 3: create with validation
- `f097971` Stage 4: full CRUD
- `c53cf0b` Stage 5: Swagger UI
- `Stage 6: publish and docs`
