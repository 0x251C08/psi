# ${project_name}

A Flask project initialized with Psi.

## Quick Start

```bash
# Install dependencies
uv sync

# Run development server
uv run flask run
# or
uv run python app.py
```

## Project Structure

```
${project_name}/
├── app.py           # Flask application
├── pyproject.toml   # Project configuration
└── tests/           # Test files
```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /items` - Create item
- `GET /items/<item_id>` - Get item

## Development

```bash
# Run tests
uv run pytest

# Lint
uv run ruff check .

# Type check
uv run mypy .
```