# ${project_name}

A Python library initialized with Psi.

## Quick Start

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest
```

## Project Structure

```
${project_name}/
├── src/${project_name}/
│   ├── __init__.py
│   └── core.py
├── tests/
│   └── test_core.py
└── pyproject.toml
```

## Usage

```python
from ${project_name} import hello, add

print(hello("World"))  # Hello, World!
print(add(2, 3))       # 5
```

## Development

```bash
# Run tests with coverage
uv run pytest --cov=${project_name}

# Lint
uv run ruff check .

# Type check
uv run mypy .

# Build package
uv build
```