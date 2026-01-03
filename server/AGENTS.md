# AGENTS.md

This file contains guidelines and commands for agentic coding assistants working in this repository.

## Project Overview

Pi Security Camera API - FastAPI backend for managing Raspberry Pi security cameras.
Tech stack: FastAPI, SQLAlchemy 2.0, PostgreSQL/SQLite, Pydantic, Python 3.13+

## Commands

### Dependencies
```bash
uv sync                        # Install all dependencies (including dev group)
uv add "package-name"          # Add a new dependency to the project
uv add --dev "package-name"    # Add a new development dependency
```

### Running the Application
```bash
uv run main.py                 # Run FastAPI server
uv run fastapi --reload        # Run with auto-reload on file changes
```

### Code Quality
```bash
uv run --dev ruff check        # Lint code
uv run --dev ruff format       # Format code
uv run --dev mypy .            # Type check (strict mode enabled)
```

### Testing
```bash
uv run --dev pytest                        # Run all tests
uv run --dev pytest tests/                 # Run all tests in tests directory
uv run --dev pytest tests/core/security/   # Run tests in specific directory
uv run --dev pytest tests/core/security/test_hashing.py           # Run specific test file
uv run --dev pytest tests/core/security/test_hashing.py::test_generate_hashed_password  # Run single test
uv run --dev pytest -k <keyword>          # Run tests matching keyword
uv run --dev pytest -x                    # Stop on first failure
uv run --dev pytest -v                    # Verbose output
```

## Code Style Guidelines

### Type System (Strict Mode)
- Full type annotations required on all functions and methods
- Use modern Python syntax: `list[Type]`, `dict[K,V]`, `set[T]` instead of `List`, `Dict`, `Set`
- Use union syntax: `Type | None` instead of `Optional[Type]`
- Always annotate return types, even if `None`
- Use `Annotated[Type, ...]` for FastAPI dependencies

### FastAPI Specific Patterns
- Dependency injection: `db_session: Annotated[Session, Depends(get_db)]`
- Path parameters: `id: Annotated[int, Path(ge=1)]`
- Query parameters: `name: Annotated[str | None, Query(regex=camera_name_regex)] = None`
- Request bodies: `camera: Annotated[CameraCreate, Body()]`
- Raise `HTTPException(status_code, detail="message")` for API errors
- Use `response_model` in route decorators for response validation

### Naming Conventions
- Variables and functions: `snake_case`
- Classes: `PascalCase`
- Constants: `ALL_CAPS`
- Private attributes: `_single_underscore`
- Module files: `snake_case.py`

### Formatting and Style
- Line length: 120 characters (enforced by ruff)
- Use Google-style docstrings (enforced by ruff pydocstyle)
- Double quotes for strings and docstrings
- Single quotes for string regex patterns
- No trailing whitespace
- One blank line between function definitions, two between class definitions

### Imports
- Standard library imports first
- Third-party imports second
- Local application imports third
- Each group separated by blank line
- Sorted alphabetically (enforced by isort via ruff)
- Use absolute imports: `from app.api.models import cameras`

### Architecture and File Organization
- `app/api/models/` - Pydantic models for request/response validation
- `app/api/routes/` - FastAPI route handlers (thin layer, delegate to services)
- `app/services/` - Business logic and CRUD operations
- `app/db/db_models.py` - SQLAlchemy ORM models
- `app/db/database.py` - Database connection and session management
- `app/core/validation/` - Regex patterns and validation utilities
- `app/core/security/` - Security-related functions (hashing, etc.)
- `tests/` - Mirror the `app/` structure for test files

### Database Patterns (SQLAlchemy 2.0)
- Use SQLAlchemy 2.0 style queries: `select(Table).where(Table.id == id)`
- ORM models use `Mapped[Type]` and `mapped_column()`
- Relationships use `Mapped[list[Type]] = relationship(...)`
- Always use type annotations with `Session` parameters
- Use `db.execute(query).scalars().all()` for selecting multiple results
- Use `db.execute(query).scalar_one_or_none()` for single results
- Commit changes explicitly: `db.commit()`, `db.refresh(obj)`

### Error Handling
- Services layer: Raise `ValueError` for validation failures
- Routes layer: Catch service errors and raise `HTTPException` with appropriate status codes
- Common status codes: 400 (bad request), 404 (not found), 409 (conflict), 500 (server error)

### Pydantic Models
- Use `BaseModel` for request/response models
- Use `Field()` for validation: `id: int = Field(ge=1)`
- Use `Field(default=None)` for optional fields in create models
- Use `Field(default=None, pattern=regex)` for validation
- Separate models for Create, Update, and Response
- Response models should exclude sensitive fields (e.g., passwords)
- Set `from_attributes: bool = True` in Config for ORM compatibility

### Testing
- Use pytest for all testing
- Test files: `test_*.py` in `tests/` directory
- Test functions: `def test_<description>()`
- Use `pytest.raises(Exception)` for exception testing
- Keep tests focused and independent
- Use descriptive test names

### Environment Variables
- `DB_TYPE` - Database type: "sqlite" or "postgres" (default: "sqlite")
- `DATABASE_URL` - Database connection string (required for postgres)

### General Principles
- Always validate input data (use Pydantic models)
- Never expose secrets or keys in logs or error messages
- Keep functions focused and single-purpose
- Prefer explicit over implicit
- Use type hints to improve IDE support and catch errors early
- Run `uv run --dev ruff format` before committing
- Run `uv run --dev mypy .` before committing to ensure type safety
- Run `uv run --dev pytest` before committing to ensure tests pass
