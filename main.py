from typing import Optional

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

app = FastAPI(title="Task API", version="1.0")


class TaskIn(BaseModel):
    title: str = ""
    done: bool = False


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Write README", "done": False},
    {"id": 3, "title": "Learn FastAPI", "done": True},
]
next_id = 4


@app.get("/", description="API info: name, version, available endpoints.")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", description="Liveness check for the server.")
def health():
    return {"status": "ok"}


@app.get("/tasks", description="List all tasks.")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}", description="Get one task by id. 404 if it doesn't exist.")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    description="Create a task. Requires a non-empty title; done defaults to false.",
)
def create_task(body: TaskIn):
    global next_id
    if not body.title.strip():
        raise HTTPException(status_code=400, detail="title is required")
    task = {"id": next_id, "title": body.title, "done": False}
    tasks.append(task)
    next_id += 1
    return task


@app.put(
    "/tasks/{task_id}",
    description="Update a task's title and/or done status. 404 if unknown id.",
)
def update_task(task_id: int, body: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if body.title is not None and not body.title.strip():
                raise HTTPException(status_code=400, detail="title cannot be empty")
            if body.title is not None:
                task["title"] = body.title
            if body.done is not None:
                task["done"] = body.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a task. 404 if unknown id.",
)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
