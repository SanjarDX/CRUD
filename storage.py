tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Write README", "done": False},
    {"id": 3, "title": "Learn FastAPI", "done": True},
]
_next_id = 4


def get_next_id() -> int:
    global _next_id
    value = _next_id
    _next_id += 1
    return value


def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None
