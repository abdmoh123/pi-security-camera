# Pi Security Camera API

API for managing Pi cameras and videos.

## Main dependencies

- fastapi
  - Includes Pydantic for data validation
  - python-multipart was also required for file uploading/downloading
- psycopg2 for Postgres
- sqlalchemy as ORM
- aiofiles for asynchronous file reading/writing
- For the full list/tree, run `uv tree`

## Dev tools used

- mypy in strict mode for type checking
- ruff for linting and formatting
- debugpy as debugger in neovim

## How to setup

### Server-side

1. Install `uv`

2. Run `uv sync` to install the required dependencies

3. Set the following environment variables
    - DB_TYPE
        - Examples include `sqlite` and `postgres`
    - DATABASE_URL
        - Will depend on the database type you use

4. To run the project, you can use `uv run main.py` or run the fastapi cli through `uv run fastapi --reload`
    - The `--reload` flag will reload the server whenever you save any changes
