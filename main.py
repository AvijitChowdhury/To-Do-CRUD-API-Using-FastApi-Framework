# ============================================================
# STAGE 0 — Hello, server
# FastAPI is the framework. It handles routing, JSON parsing,
# validation, and gives us Swagger UI for free.
# ============================================================

from fastapi import FastAPI, HTTPException  # FastAPI = the app; HTTPException = how we send error responses
from pydantic import BaseModel              # Pydantic validates incoming JSON automatically
from typing import Optional                # Optional means a field can be None (missing)

# ============================================================
# Create the app
# FastAPI() builds your server object. title/description/version
# appear in the Swagger UI at /docs — free documentation.
# ============================================================
app = FastAPI(
    title="Task API",
    description="A simple to-do list API — full CRUD, in-memory storage.",
    version="1.0",
)


# ============================================================
# STAGE 2 — The "database" (in-memory list)
# A plain Python list. No database yet — data lives in RAM.
# It disappears when the server restarts. That's intentional.
# ============================================================

# Each task is a dict with three fields:
#   id    — unique number, we assign it
#   title — text the user provides
#   done  — True/False, starts False
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Read a book",   "done": True},
    {"id": 3, "title": "Go for a walk", "done": False},
]

# A counter so every new task gets a unique id.
# We never reuse ids — even if a task is deleted.
next_id = 4   # tasks 1, 2, 3 exist, so the next free id is 4


# ============================================================
# Pydantic models — the "shape" of incoming JSON
# When a client POSTs or PUTs, FastAPI reads the request body
# and checks it matches this model. Wrong type or missing
# required field → automatic 422 error, no code from us.
# ============================================================

class TaskCreate(BaseModel):
    """Body expected when creating a task (POST /tasks)."""
    title: str                  # required — must be a string
    # 'done' is not here; we always set it to False on creation

class TaskUpdate(BaseModel):
    """Body expected when updating a task (PUT /tasks/{id}).
    Both fields are Optional so the client can send just one."""
    title: Optional[str] = None   # may be missing → None
    done:  Optional[bool] = None  # may be missing → None


# ============================================================
# Helper — find a task by id
# Searching a list in Python: next() returns the first match,
# or None if nothing matches.
# ============================================================

def find_task(task_id: int):
    return next((t for t in tasks if t["id"] == task_id), None)
    # Read aloud: "return the first t in tasks where t['id'] equals
    # task_id; if none found, return None"


# ============================================================
# STAGE 1 — Root and health endpoints
# These two endpoints are not about tasks; they describe the
# server and let monitoring tools check it is alive.
# ============================================================

@app.get("/")                           # @app.get("/") = "when GET / arrives, call this function"
def root():
    """Describes the API."""
    return {                             # FastAPI converts this dict to JSON automatically
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }

@app.get("/health")
def health():
    """Health-check — real companies poll this to know the server is running."""
    return {"status": "ok"}


# ============================================================
# STAGE 2 — Read endpoints
# GET /tasks        → all tasks
# GET /tasks/{id}   → one task (or 404)
# ============================================================

@app.get("/tasks", summary="List all tasks")
def list_tasks():
    """Returns every task in the in-memory list."""
    return tasks                         # the whole list, converted to a JSON array

@app.get("/tasks/{task_id}", summary="Get one task")
def get_task(task_id: int):              # {task_id} in the path becomes an int argument
    """Returns a single task by id, or 404 if not found."""
    task = find_task(task_id)
    if task is None:
        # HTTPException tells FastAPI: send this status code + detail as JSON
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


# ============================================================
# STAGE 3 — Create endpoint
# POST /tasks — client sends {"title": "Buy milk"}
# We assign an id, set done=False, add to list, return 201.
# ============================================================

@app.post("/tasks", status_code=201, summary="Create a task")
def create_task(body: TaskCreate):       # FastAPI parses + validates the request body for us
    """Creates a new task. Title is required. Returns 201 with the created task."""
    global next_id                       # 'global' lets us modify the counter defined outside

    # Extra validation: Pydantic accepts an empty string as a valid str,
    # so we add our own business rule: title must not be blank.
    if not body.title.strip():           # .strip() removes whitespace; empty after strip → reject
        raise HTTPException(status_code=400, detail="title must not be empty")

    new_task = {
        "id":    next_id,
        "title": body.title.strip(),     # store without leading/trailing spaces
        "done":  False,                  # always False on creation
    }
    tasks.append(new_task)               # add to our in-memory "database"
    next_id += 1                         # bump the counter for the next task
    return new_task                      # FastAPI returns this as JSON with status 201


# ============================================================
# STAGE 4 — Update endpoint
# PUT /tasks/{id} — client sends {"title": "...", "done": true}
# We patch only the fields the client sent. Returns the task.
# ============================================================

@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, body: TaskUpdate):
    """Updates title and/or done. Unknown id → 404. Empty body → 400."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    # body.title is None if the client didn't send it → don't touch the field
    if body.title is not None:
        if not body.title.strip():
            raise HTTPException(status_code=400, detail="title must not be empty")
        task["title"] = body.title.strip()

    if body.done is not None:
        task["done"] = body.done         # True or False — valid either way

    # Check the client sent at least one field
    if body.title is None and body.done is None:
        raise HTTPException(status_code=400, detail="send at least one of: title, done")

    return task                          # 200 OK with the updated task


# ============================================================
# STAGE 4 — Delete endpoint
# DELETE /tasks/{id} → remove task, return 204 No Content
# 204 means "success, nothing to say back" — no body at all.
# ============================================================

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    """Deletes a task by id. Returns 204 on success, 404 if not found."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    tasks.remove(task)                   # remove the dict object from the list
    return                               # no return value → FastAPI sends an empty 204 body


# ============================================================
# BONUS STRETCH — Stats and filter
# GET /stats                   → total / done / open counts
# GET /tasks?done=true         → filter tasks by status
# GET /tasks?search=milk       → filter tasks by title keyword
# ============================================================

@app.get("/stats", summary="Task statistics")
def stats():
    """Returns totals: how many tasks, how many done, how many open."""
    done_count = sum(1 for t in tasks if t["done"])   # count True values
    return {
        "total": len(tasks),
        "done":  done_count,
        "open":  len(tasks) - done_count,
    }

# We override list_tasks above to add optional query parameters.
# (Re-defined below — remove the first @app.get("/tasks") if you use this version.)
# Commented out because the simple version above is already registered.
# Uncomment this block AND comment out the simple list_tasks above to use filtering.

# @app.get("/tasks", summary="List all tasks (with optional filter)")
# def list_tasks(done: Optional[bool] = None, search: Optional[str] = None):
#     result = tasks
#     if done is not None:
#         result = [t for t in result if t["done"] == done]
#     if search:
#         result = [t for t in result if search.lower() in t["title"].lower()]
#     return result


# ============================================================
# Run with:   uvicorn main:app --reload
# Then visit: http://localhost:8000/docs  ← Swagger UI
#             http://localhost:8000/      ← root JSON
# ============================================================
