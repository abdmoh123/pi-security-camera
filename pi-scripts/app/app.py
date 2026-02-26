from fastapi import FastAPI

from app.api.routes import functions

app = FastAPI(
    title="Pi Security Camera",
    description="API for controlling a Pi camera device",
)

app.include_router(functions.router)


@app.get("/")
def read_root() -> dict[str, str]:
    """Root API function."""
    return {"message": app.title, "description": app.description}


@app.get("/health")
def check_health() -> dict[str, str]:
    """Route to check health. Doesn't really do anything yet."""
    return {"status": "ok"}
