import db
from errors import InvalidTitleError, TaskNotFoundError
from models import TaskIn, TaskUpdate


def list_tasks() -> list[dict]:
    return db.list_tasks()


def get_task(task_id: int) -> dict:
    task = db.get_task(task_id)
    if task is None:
        raise TaskNotFoundError(task_id)
    return task


def create_task(body: TaskIn) -> dict:
    if not body.title.strip():
        raise InvalidTitleError("title is required")
    return db.create_task(body.title)


def update_task(task_id: int, body: TaskUpdate) -> dict:
    if body.title is not None and not body.title.strip():
        raise InvalidTitleError("title cannot be empty")
    task = db.update_task(task_id, body.title, body.done)
    if task is None:
        raise TaskNotFoundError(task_id)
    return task


def delete_task(task_id: int) -> None:
    deleted = db.delete_task(task_id)
    if not deleted:
        raise TaskNotFoundError(task_id)
