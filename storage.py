from itertools import count

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Write README", "done": False},
    {"id": 3, "title": "Learn FastAPI", "done": True},
]
_id_counter = count(4)


def get_next_id() -> int:
    return next(_id_counter)


def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None
