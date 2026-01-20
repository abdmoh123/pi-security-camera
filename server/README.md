# Pi Security Camera API server

FastAPI based API for managing Pi cameras and videos.

## Dev tools used

- mypy in strict mode for type checking
- ruff for linting and formatting
- debugpy as debugger in neovim

## How to setup

1. Install `uv`

2. Run `uv sync` to install the required dependencies

3. Set the following required environment variables
    - DB_TYPE
        - Examples include `sqlite` and `postgres`
    - POSTGRES related env variables (if DB_TYPE is `postgres`)
        - For example POSTGRES_USER and POSTGRES_PASSWORD
    - SECRET_KEY
        - Generate using `openssl rand -hex 32`

4. Set any optional environment variables
    - JWT_ALGORITHM
        - Default is HS256
    - ACCESS_TOKEN_EXPIRE_MINUTES
        - Default is 30 mins
    - REFRESH_TOKEN_EXPIRE_DAYS
        - Default is 30 days
    - ENABLE_FIRST_USER_ADMIN
        - Default is true (so we can easily have an admin user)

5. To run the project, you can use `uv run main.py` or run the fastapi cli through `uv run fastapi --reload`
    - The `--reload` flag will reload the server whenever you save any changes
