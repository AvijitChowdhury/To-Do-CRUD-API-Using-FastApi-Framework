# Task API — FlyRank AI Internship Week 2 Assignment

This repository contains a lightweight REST API for managing tasks. It was built as my first hands-on assignment during the FlyRank AI internship program, focusing on backend development fundamentals with FastAPI.

## Overview

The Task API is a simple to-do application that supports full CRUD operations using an in-memory list. It demonstrates core API concepts such as routing, request handling, JSON responses, and interactive documentation through Swagger UI.

## Features

- Create, read, update, and delete tasks
- Retrieve task statistics
- Health check endpoint for monitoring
- Automatic API documentation at `/docs`
- Lightweight setup with Python and FastAPI

## Tech Stack

- Python
- FastAPI
- Uvicorn

## Project Structure

```text
todo-api/
├── main.py      # API routes and application logic
└── README.md    # Project documentation
```

## Setup Instructions

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the environment

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn
```

### 4. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:
- http://localhost:8000
- Swagger UI: http://localhost:8000/docs

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/{id}` | Retrieve a single task |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task |
| GET | `/stats` | Retrieve task statistics |

## Example Requests

```bash
# List all tasks
curl -i http://localhost:8000/tasks

# Get task 1
curl -i http://localhost:8000/tasks/1

# Create a task
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk"}'

# Update task 1
curl -i -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Delete task 2
curl -i -X DELETE http://localhost:8000/tasks/2

# Get statistics
curl -i http://localhost:8000/stats
```

## Sample Response

```http
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Notes

The task list is stored in memory, so all data will be lost when the server restarts. The application reloads the initial seed tasks on startup, which makes it ideal for learning and testing API behavior.

## Architecture Workflow

The Task API follows a simple end-to-end request lifecycle that can be understood as a sequence of client → API → business logic → storage → response.

```mermaid
flowchart LR
    A[Client / Browser / curl] --> B[FastAPI Application]
    B --> C[Route Handler]
    C --> D[In-Memory Task List]
    D --> E[JSON Response]
    E --> F[Swagger UI /docs]
    F --> G[Playwright Python E2E Tests]
    G --> H[Allure-style Test Evidence]
```

### How the workflow works

1. A client sends an HTTP request such as GET, POST, PUT, or DELETE to the FastAPI server.
2. FastAPI routes the request to the matching endpoint function inside the application.
3. The route handler reads or updates the in-memory task list and applies basic validation rules.
4. The API returns a JSON response with task details, status codes, or error messages.
5. Swagger UI at `/docs` provides an interactive interface for manual testing.
6. Playwright Python executes the workflow end to end and captures screenshots for documentation and evidence.

This architecture is intentionally lightweight, making it ideal for learning REST API design and API test automation fundamentals.

## API Testing Screenshots

### 1. API landing page
![API landing page](assests/1.png)

### 2. Swagger UI
![Swagger UI](assests/2_SwaggerUI.png)

### 3. Health check endpoint
![Health check endpoint](assests/3_get_health_check.png)

### 4. Get all tasks
![Get all tasks](assests/4_get_tasks.png)

### 5. Create a new task
![Create a new task](assests/5_post_tasks.png)

### 6. Get a task by ID
![Get a task by ID](assests/6_get_tasks_with_id.png)

### 7. Update a task
![Update a task](assests/7_updating_tasks.png)

### 8. Delete a task by ID
![Delete a task by ID](assests/8_delete_with_id.png)

### 9. Get statistics
![Get statistics](assests/9_get_statistics.png)

## Playwright Python POM Testing

A dedicated Python-based Playwright suite was added under the [playwright_python](playwright_python) folder to exercise the API end to end using a page-object model structure.

### Test structure

```text
playwright_python/
├── pages/
│   ├── base_page.py
│   └── task_api_page.py
└── tests/
    └── test_api_workflow.py
```

### What the Playwright E2E flow validates

- Health check endpoint responds successfully
- Task creation works with a valid payload
- Task retrieval returns the expected item
- Task update changes the completion state correctly
- Statistics endpoint reports the correct counts
- Task deletion removes the item and returns a 404 on subsequent lookup

### Screenshots captured by the Playwright POM workflow

- Landing page screenshot: [assests/playwright_python/landing_page_python.png](assests/playwright_python/landing_page_python.png)
- Swagger UI screenshot: [assests/playwright_python/swagger_ui_python.png](assests/playwright_python/swagger_ui_python.png)

### Allure-style reporting notes

The Playwright Python workflow is designed to produce visual evidence for each API scenario. The captured screenshots are stored in [assests/playwright_python](assests/playwright_python) and can be used as documentation artifacts or attached to an Allure-style test report when integrated with a reporting pipeline.

### End-to-end API testing summary

This repository now demonstrates a complete testing story:

1. Manual API testing screenshots are preserved in [assests](assests).
2. Playwright Python automation exercises the same API flow end to end.
3. Visual evidence is captured in [assests/playwright_python](assests/playwright_python).
4. The README serves as a central place to review both the API behavior and the test evidence.

