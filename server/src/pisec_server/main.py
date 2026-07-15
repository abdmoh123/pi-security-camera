"""Pi security project main entrypoint."""

from importlib.metadata import PackageNotFoundError, version

import typer
import uvicorn
from fastapi import FastAPI

from pisec_server.api.routes import cameras, users, videos
from pisec_server.auth import routes as auth

# get version info
try:
    # get version from installed package metadata
    __version__ = version("pisec-server")
except PackageNotFoundError:
    # package is not installed (e.g. in development without editable install)
    __version__ = "0.1.0"  # fallback initial version value

app = FastAPI(title="Pi Security Camera", description="API for managing Pi security cameras", version=__version__)

api_prefix: str = "/api/v0"
app.include_router(users.router, prefix=api_prefix)
app.include_router(cameras.router, prefix=api_prefix)
app.include_router(videos.router, prefix=api_prefix)
app.include_router(auth.router, prefix=api_prefix)


@app.get(api_prefix)
def read_root() -> dict[str, str]:
    """Root API function."""
    return {"message": app.title, "description": app.description, "version": app.version}


@app.get(f"{api_prefix}/health")
def check_health() -> dict[str, str]:
    """Route to check health. Doesn't really do anything yet."""
    return {"status": "ok"}


cli_app = typer.Typer()


@cli_app.command()
def serve(host: str = "127.0.0.1", port: int = 8000, reload: bool = True) -> None:
    """Main file entrypoint."""
    uvicorn.run("pisec_server.main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    cli_app()
