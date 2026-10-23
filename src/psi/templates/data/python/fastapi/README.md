# ${project_name}

A FastAPI project initialized with Psi.

## Quick Start

```bash
# Install dependencies
uv sync

# Run development server
uv run uvicorn main:app --reload
```

## Project Structure

```
${project_name}/
├── main.py          # FastAPI application
├── pyproject.toml   # Project configuration
└── tests/           # Test files
```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /items` - Create item
- `GET /items/{item_id}` - Get item

## Development

```bash
# Run tests
uv run pytest

# Lint
uv run ruff check .

# Type check
uv run mypy .
```