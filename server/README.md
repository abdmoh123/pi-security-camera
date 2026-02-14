# Pi Security Camera API server

FastAPI based API for managing Pi cameras and videos.

## Tooling

### Linting and formatting

- mypy in strict mode for type checking
- ruff for linting and formatting

### Testing

- pytest for running unit tests

### IDE specific

#### Neovim

- debugpy as debugger
- basedpyright as lsp

## How to setup

### Installing dependencies

Install `uv` then run `uv sync` to install the required dependencies.

### Environment variables

All environment variables are loaded and accessed from the app.core.config module.

#### Required

- DB_TYPE
    - Examples include `sqlite` and `postgres`
- POSTGRES related env variables (if DB_TYPE is `postgres`)
    - For example POSTGRES_USER and POSTGRES_PASSWORD
- SECRET_KEY
    - Generate using `openssl rand -hex 32`
    - Used for encoding JWT tokens

#### Optional

- JWT_ALGORITHM
    - Default is HS256
- ACCESS_TOKEN_EXPIRE_MINUTES
    - Default is 30 mins
- REFRESH_TOKEN_EXPIRE_DAYS
    - Default is 30 days
- ENABLE_FIRST_USER_ADMIN
    - Default is true (so we can easily setup an admin user)

#### Other

- DOCKER_PATH
    - Used by mise devcontainer task to allow users to choose docker alternatives like podman

> [!TIP]
> You can use the `.env` file to set these environment variables, as the application uses dotenv to load them.

## Running the project

To run the project, you can use `uv run main.py` or run the fastapi cli through `uv run fastapi --reload`.
The `--reload` flag will reload the server whenever you save any changes.
