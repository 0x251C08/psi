# ${project_name}

A Django project initialized with Psi.

## Quick Start

```bash
# Install dependencies
uv sync

# Run migrations
uv run python manage.py migrate

# Create superuser (optional)
uv run python manage.py createsuperuser

# Run development server
uv run python manage.py runserver
```

## Project Structure

```
${project_name}/
├── manage.py              # Django management script
├── pyproject.toml         # Project configuration
├── ${project_name}/       # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── core/                  # Core app
    ├── models.py
    ├── views.py
    ├── serializers.py
    └── urls.py
```

## API Endpoints

- `GET /api/items/` - List items
- `POST /api/items/` - Create item
- `GET /api/items/{id}/` - Get item
- `PUT /api/items/{id}/` - Update item
- `DELETE /api/items/{id}/` - Delete item

## Development

```bash
# Run tests
uv run pytest

# Lint
uv run ruff check .

# Type check
uv run mypy .

# Create new migration
uv run python manage.py makemigrations
```