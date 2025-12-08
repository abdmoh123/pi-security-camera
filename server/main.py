"""Pi security project main entrypoint."""

from importlib.metadata import PackageNotFoundError, version

import uvicorn
from fastapi import FastAPI

from app.api.routes import cameras, users

# get version info
try:
    # get version from installed package metadata
    __version__ = version("pi-security-camera")
except PackageNotFoundError:
    # package is not installed (e.g. in development without editable install)
    __version__ = "0.1.0"  # fallback initial version value

app = FastAPI(title="Pi Security Camera", description="API for managing Pi security cameras", version=__version__)

api_prefix: str = "/api/v0"
app.include_router(users.router, prefix=api_prefix)
app.include_router(cameras.router, prefix=api_prefix)


@app.get(api_prefix)
def read_root() -> dict[str, str]:
    """Root API function."""
    return {"message": app.title, "description": app.description, "version": app.version}


@app.get(f"{api_prefix}/health")
def check_health() -> dict[str, str]:
    """Route to check health. Doesn't really do anything yet."""
    return {"status": "ok"}


def main(reload: bool = True) -> None:
    """Main file entrypoint."""
    uvicorn.run("main:app", reload=reload)


if __name__ == "__main__":
    main()
