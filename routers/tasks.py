from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

import services.task_service as task_service
from errors import InvalidTitleError, TaskNotFoundError
from models import TaskIn, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", description="List all tasks.")
async def list_tasks():
    return task_service.list_tasks()


@router.get("/{task_id}", description="Get one task by id. 404 if it doesn't exist.")
async def get_task(task_id: int):
    try:
        return task_service.get_task(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    description="Create a task. Requires a non-empty title; done defaults to false.",
)
async def create_task(body: TaskIn):
    try:
        return task_service.create_task(body)
    except InvalidTitleError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.put(
    "/{task_id}",
    description="Update a task's title and/or done status. 404 if unknown id.",
)
async def update_task(task_id: int, body: TaskUpdate):
    try:
        return task_service.update_task(task_id, body)
    except InvalidTitleError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a task. 404 if unknown id.",
)
async def delete_task(task_id: int):
    try:
        task_service.delete_task(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
