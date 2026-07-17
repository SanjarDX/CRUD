from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from models import TaskIn, TaskUpdate
from storage import tasks, find_task, get_next_id

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", description="List all tasks.")
async def list_tasks():
    return tasks


@router.get("/{task_id}", description="Get one task by id. 404 if it doesn't exist.")
async def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    description="Create a task. Requires a non-empty title; done defaults to false.",
)
async def create_task(body: TaskIn):
    if not body.title.strip():
        raise HTTPException(status_code=400, detail="title is required")
    task = {"id": get_next_id(), "title": body.title, "done": False}
    tasks.append(task)
    return task


@router.put(
    "/{task_id}",
    description="Update a task's title and/or done status. 404 if unknown id.",
)
async def update_task(task_id: int, body: TaskUpdate):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    if body.title is not None and not body.title.strip():
        raise HTTPException(status_code=400, detail="title cannot be empty")
    if body.title is not None:
        task["title"] = body.title
    if body.done is not None:
        task["done"] = body.done
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a task. 404 if unknown id.",
)
async def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    tasks.remove(task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
