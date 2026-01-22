"""Pi security project main entrypoint."""

import uvicorn

# Allows the main method to run the fast api application
from app.app import app  # noqa: F401  # pyright: ignore[reportUnusedImport]


def main(reload: bool = True) -> None:
    """Main file entrypoint."""
    uvicorn.run("main:app", reload=reload)


if __name__ == "__main__":
    main()
