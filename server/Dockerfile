FROM docker.io/ubuntu:24.04

# Create and switch to work directory
WORKDIR /usr/src/pi-security-camera/server

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Installs dependencies via uv venv
COPY pyproject.toml uv.lock .
RUN uv sync --frozen

# Copies the source code in
COPY . .

# Run FastAPI server
CMD ["uv", "run", "fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]
