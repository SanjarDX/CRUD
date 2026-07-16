# Task API

Small CRUD API for a to-do list. In-memory storage only — data resets on every restart. Built with FastAPI as W2·A1.

## Run it

```bash
python -m venv venv
venv/Scripts/pip install -r requirements.txt
venv/Scripts/python -m uvicorn main:app --port 8000
```

Server: `http://localhost:8000` · Swagger UI: `http://localhost:8000/docs`

## Endpoints

| Method | Path | Description | Success | Errors |
|---|---|---|---|---|
| GET | `/` | API info | 200 | — |
| GET | `/health` | Liveness check | 200 | — |
| GET | `/tasks` | List all tasks | 200 | — |
| GET | `/tasks/{id}` | Get one task | 200 | 404 |
| POST | `/tasks` | Create a task (`{"title": "..."}`) | 201 | 400 (empty/missing title) |
| PUT | `/tasks/{id}` | Update title and/or done | 200 | 400, 404 |
| DELETE | `/tasks/{id}` | Delete a task | 204 | 404 |

## Example

```
$ curl -i http://localhost:8000/tasks/1
HTTP/1.1 200 OK
content-type: application/json

{"id":1,"title":"Buy milk","done":false}
```

## Swagger UI

Full CRUD cycle tested via "Try it out" at `/docs`:

![Swagger UI](docs/swagger.png)

## Mortality experiment

Created a few tasks, restarted the server, `GET /tasks` came back with only the original 3 seed tasks. Data lives in a Python list in process memory — once the process exits, that memory is gone. This is exactly why Week 3 introduces a real database.
