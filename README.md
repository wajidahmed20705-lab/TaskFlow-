# TaskFlow - Modern FastAPI CRUD & Interactive Web Dashboard

A fast, lightweight, and modern **Task Management API & Web Dashboard** built with **Python 3.14**, **FastAPI**, **Uvicorn**, and **Vanilla HTML5/CSS3/JavaScript**.

Featuring interactive **Swagger OpenAPI Documentation** (`/docs`), real-time **HTTP activity logging**, search and filtering, and an in-memory RESTful engine.

![TaskFlow UI Banner](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

---

## ✨ Features

- ⚡ **High Performance REST API**: Full CRUD endpoints for managing tasks.
- 🎨 **Modern Dark Dashboard**: Glassmorphic UI with smooth micro-animations, statistics widgets, search bar, and filter tabs.
- 📜 **Interactive Swagger Docs**: Built-in OpenAPI testing environment available at `/docs`.
- 🩺 **Health & System Endpoints**: `/health` status check, `/stats` counter summary, and `/reset` data restoring.
- 🛠️ **Live HTTP Activity Inspector**: Visual log terminal embedded in the web UI showing real-time REST requests & response codes.
- 🛡️ **Robust Validation & Status Codes**: Standard REST compliance (`200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `404 Not Found`).

---

## 🚀 Quick Start

### 1. Clone & Setup Environment

```bash
git clone https://github.com/your-username/taskflow-fastapi.git
cd taskflow-fastapi
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Development Server

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Open your browser and navigate to:
- 🌐 **Web Dashboard**: `http://localhost:8000`
- 📖 **Swagger UI Documentation**: `http://localhost:8000/docs`
- ⚡ **API Meta Endpoint**: `http://localhost:8000/api`

---

## 📌 REST API Endpoint Reference

| Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Serves the interactive Web Dashboard UI | `200 OK` |
| `GET` | `/api` | Returns API name, version, and endpoints list | `200 OK` |
| `GET` | `/health` | Health check endpoint for uptime monitors | `200 OK` |
| `GET` | `/tasks` | List all tasks (supports `?done=true` and `?search=kw`) | `200 OK` |
| `GET` | `/tasks/{id}` | Retrieve a specific task by numeric ID | `200 OK`, `404 Not Found` |
| `POST` | `/tasks` | Create a new task (body: `{"title": "Buy milk"}`) | `201 Created`, `400 Bad Request` |
| `PUT` | `/tasks/{id}` | Update task title or completed status | `200 OK`, `400 Bad Request`, `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Delete task by numeric ID | `204 No Content`, `404 Not Found` |
| `GET` | `/stats` | Returns counter statistics (`total`, `done`, `open`) | `200 OK` |
| `POST` | `/reset` | Restores default sample data | `200 OK` |

---

## 💻 Example `curl` Commands

### Create a Task
```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Build a FastAPI Web Dashboard"}'
```

### List Tasks with Search Filter
```bash
curl -i "http://localhost:8000/tasks?search=FastAPI&done=false"
```

### Update Task Status
```bash
curl -i -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

### Delete a Task
```bash
curl -i -X DELETE http://localhost:8000/tasks/1
```

---

## 📁 Project Structure

```text
├── main.py              # FastAPI application server & route handlers
├── static/
│   └── index.html       # Single-page web dashboard application
├── requirements.txt     # Python package dependencies
├── .gitignore           # Git ignore settings
└── README.md            # Project documentation
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
