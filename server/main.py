"""Pi security project main entrypoint."""

from fastapi import FastAPI

from app.database import engine
from app.db_models import Base

from app.routes import cameras, users


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pi Security Camera", description="API for managing Pi security cameras", version="0.1.0")

app.include_router(users.router, prefix="/api/v0")
app.include_router(cameras.router, prefix="/api/v0")


@app.get("/api/v0")
def read_root() -> dict[str, str]:
    """Root API function."""
    return {"message": app.title, "description": app.description, "version": app.version}


@app.get("/api/v0/health")
def check_health() -> dict[str, str]:
    """Route to check health. Doesn't really do anything yet."""
    return {"status": "ok"}
