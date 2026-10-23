# Psi

Developer quality-of-life tool for codebase inspection and project initialization.

## Features

- **`psi inspect`** - Inspect a codebase: git repo, dependencies, tool versions, and project structure
- **`psi init`** - Initialize new projects in various languages and frameworks
- **Interactive TUI** - Visual project initialization with `psi init --interactive`

## Installation

```bash
# From source
uv pip install -e .

# Or with pip
pip install -e .
```

## Usage

### Inspect a codebase

```bash
# Inspect current directory
psi inspect

# Inspect specific path
psi inspect /path/to/project

# Output as JSON for automation
psi inspect --json

# Verbose output (deeper structure)
psi inspect -v
```

### Initialize a new project

```bash
# Interactive mode (TUI)
psi init --interactive

# Non-interactive with language
psi init python
psi init zig
psi init rust
psi init go
psi init node
psi init webdev

# Specify project name and path
psi init python --name my-api --path /tmp/projects

# Webdev with framework
psi init webdev --name my-app  # Will prompt for framework
```

### Supported Languages & Frameworks

| Language | Frameworks |
|----------|------------|
| **Python** | fastapi, flask, django, cli, library |
| **Zig** | exe, lib |
| **Rust** | bin, lib, axum, actix, cli |
| **Go** | mod, cli, web |
| **Node.js** | npm, cli, web (express), fastify |
| **Webdev** | vanilla, typescript, react, vue, svelte, solid, astro, next, nuxt |

Webdev frameworks (except vanilla/typescript) support CSS options: vanilla, tailwind, bootstrap, postcss

## Examples

```bash
# Create a FastAPI project
psi init python --name my-api
# Selects fastapi by default, or use --interactive

# Create a React + Tailwind project
psi init webdev --name my-app
# Selects react in TUI, then tailwind for CSS

# Create a Rust CLI with clap
psi init rust --name my-cli
# Selects cli framework in TUI

# Inspect a codebase and get JSON output
psi inspect /path/to/repo --json
```

## Project Structure

```
src/psi/
├── cli.py              # Main CLI entry point (Typer)
├── commands/
│   ├── inspect.py      # Codebase inspection logic
│   └── init.py         # Project initialization logic
├── templates/
│   ├── __init__.py     # Template management
│   └── data/           # Project templates
├── tui/
│   └── init_tui.py     # Interactive TUI (Textual)
└── utils/
    ├── fs.py           # Filesystem utilities
    ├── dependencies.py # Dependency detection
    └── tools.py        # Tool version detection
```

## Development

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
uv run pytest

# Lint
uv run ruff check .

# Type check
uv run mypy .

# Run CLI
uv run psi --help
```

## License

MIT