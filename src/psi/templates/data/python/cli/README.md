# ${project_name}

A command-line application initialized with Psi.

## Quick Start

```bash
# Install dependencies
uv sync

# Run CLI
uv run ${project_name} --help
uv run ${project_name} hello "World"
```

## Project Structure

```
${project_name}/
├── cli.py           # CLI application (Typer)
├── pyproject.toml   # Project configuration
└── tests/           # Test files
```

## Commands

- `hello [NAME]` - Say hello
- `goodbye [NAME]` - Say goodbye
- `version` - Show version

## Development

```bash
# Run tests
uv run pytest

# Lint
uv run ruff check .

# Type check
uv run mypy .
```