from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from routers.tasks import router as tasks_router

app = FastAPI(title="Task API", version="1.0")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.get("/", description="API info: name, version, available endpoints.")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", description="Liveness check for the server.")
async def health():
    return {"status": "ok"}


app.include_router(tasks_router)
