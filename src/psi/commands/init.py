"""Project initialization logic and templates."""

import shutil
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from psi.templates import get_template, render_template

console = Console()

# Language/framework mappings
LANGUAGE_TEMPLATES: dict[str, dict[str, Any]] = {
    "python": {
        "description": "Python project",
        "frameworks": {
            "fastapi": "FastAPI web API",
            "flask": "Flask web application",
            "django": "Django web framework",
            "cli": "Command-line application (Typer)",
            "library": "Python library/package",
        },
    },
    "zig": {
        "description": "Zig project",
        "frameworks": {
            "exe": "Executable application",
            "lib": "Library",
        },
    },
    "rust": {
        "description": "Rust project",
        "frameworks": {
            "bin": "Binary application (cargo new)",
            "lib": "Library (cargo new --lib)",
            "axum": "Axum web server",
            "actix": "Actix-web server",
            "cli": "CLI application (clap)",
        },
    },
    "go": {
        "description": "Go project",
        "frameworks": {
            "mod": "Go module",
            "cli": "CLI application (cobra)",
            "web": "Web server (chi/gin)",
        },
    },
    "node": {
        "description": "Node.js project",
        "frameworks": {
            "npm": "npm package",
            "cli": "CLI application",
            "web": "Express.js server",
            "fastify": "Fastify server",
        },
    },
    "webdev": {
        "description": "Web development project",
        "frameworks": {
            "vanilla": "Vanilla HTML/CSS/JS",
            "typescript": "TypeScript project",
            "react": "React (Vite)",
            "vue": "Vue (Vite)",
            "svelte": "Svelte (Vite)",
            "solid": "SolidJS (Vite)",
            "astro": "Astro static site",
            "next": "Next.js",
            "nuxt": "Nuxt.js",
        },
        "css_options": {
            "vanilla": "Vanilla CSS",
            "tailwind": "Tailwind CSS",
            "bootstrap": "Bootstrap",
            "postcss": "PostCSS",
        },
    },
}


def init_project(
    language: str,
    target_path: Path,
    name: str | None = None,
    force: bool = False,
) -> None:
    """Initialize a new project from template."""
    language = language.lower()

    if language not in LANGUAGE_TEMPLATES:
        console.print(f"[red]Unknown language: {language}[/red]")
        console.print(f"Supported: {', '.join(LANGUAGE_TEMPLATES.keys())}")
        return

    lang_info = LANGUAGE_TEMPLATES[language]

    # If language has frameworks, ask which one
    if "frameworks" in lang_info:
        framework = _select_framework(language, lang_info)
        if not framework:
            return
    else:
        framework = "default"

    # Determine project name
    if name is None:
        name = target_path.name

    project_path = target_path / name
    if project_path.exists() and not force:
        if not Confirm.ask(f"[yellow]Directory {project_path} exists. Overwrite?[/yellow]"):
            console.print("[red]Aborted.[/red]")
            return
        shutil.rmtree(project_path)

    project_path.mkdir(parents=True, exist_ok=True)

    # Get and render template
    template = get_template(language, framework)
    if template:
        render_template(template, project_path, {"project_name": name, "language": language})
        console.print(f"[green]✓[/green] Created {language}/{framework} project at {project_path}")
        _show_next_steps(language, framework, project_path)
    else:
        console.print(f"[red]No template found for {language}/{framework}[/red]")


def _select_framework(language: str, lang_info: dict) -> str | None:
    """Prompt user to select a framework."""
    console.print(f"\n[bold]{lang_info['description']}[/bold]")
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Key", style="cyan")
    table.add_column("Framework", style="green")
    table.add_column("Description")

    for key, desc in lang_info["frameworks"].items():
        table.add_row(key, key, desc)

    console.print(table)

    framework = Prompt.ask(
        "Select framework",
        choices=list(lang_info["frameworks"].keys()),
        default=next(iter(lang_info["frameworks"].keys())),
    )

    # For webdev, also ask about CSS
    webdev_frameworks = ["vanilla", "typescript", "react", "vue", "svelte", "solid"]
    if language == "webdev" and framework in webdev_frameworks:
        css = _select_css()
        if css:
            framework = f"{framework}-{css}"

    return framework


def _select_css() -> str | None:
    """Prompt user to select CSS framework."""
    css_options = LANGUAGE_TEMPLATES["webdev"]["css_options"]

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Key", style="cyan")
    table.add_column("CSS Framework", style="green")
    table.add_column("Description")

    for key, desc in css_options.items():
        table.add_row(key, key, desc)

    console.print("\n[bold]Select CSS framework:[/bold]")
    console.print(table)

    return Prompt.ask(
        "CSS framework",
        choices=list(css_options.keys()),
        default="vanilla",
    )


def _show_next_steps(language: str, framework: str, project_path: Path) -> None:
    """Show next steps after project creation."""
    console.print("\n[bold]Next steps:[/bold]")

    steps = {
        ("python", "fastapi"): [
            f"cd {project_path}",
            "uv sync  # or pip install -e .",
            "uv run uvicorn main:app --reload",
        ],
        ("python", "flask"): [
            f"cd {project_path}",
            "uv sync",
            "uv run flask run",
        ],
        ("python", "django"): [
            f"cd {project_path}",
            "uv sync",
            "uv run python manage.py runserver",
        ],
        ("python", "cli"): [
            f"cd {project_path}",
            "uv sync",
            "uv run python -m cli",
        ],
        ("python", "library"): [
            f"cd {project_path}",
            "uv sync",
            "uv run pytest",
        ],
        ("zig", "exe"): ["cd {project_path}", "zig build run"],
        ("zig", "lib"): ["cd {project_path}", "zig build test"],
        ("rust", "bin"): ["cd {project_path}", "cargo run"],
        ("rust", "lib"): ["cd {project_path}", "cargo test"],
        ("rust", "axum"): ["cd {project_path}", "cargo run"],
        ("rust", "actix"): ["cd {project_path}", "cargo run"],
        ("rust", "cli"): ["cd {project_path}", "cargo run"],
        ("go", "mod"): ["cd {project_path}", "go run ."],
        ("go", "cli"): ["cd {project_path}", "go run ."],
        ("go", "web"): ["cd {project_path}", "go run ."],
        ("node", "npm"): ["cd {project_path}", "npm install", "npm test"],
        ("node", "cli"): ["cd {project_path}", "npm install", "npm start"],
        ("node", "web"): ["cd {project_path}", "npm install", "npm run dev"],
        ("node", "fastify"): ["cd {project_path}", "npm install", "npm run dev"],
    }

    key = (language, framework.split("-", maxsplit=1)[0])  # Handle webdev-css combos
    if key in steps:
        for step in steps[key]:
            console.print(f"  [cyan]{step.format(project_path=project_path)}[/cyan]")
    else:
        console.print(f"  [cyan]cd {project_path}[/cyan]")
        console.print("  [cyan]# Check README.md for instructions[/cyan]")


def init_project_tui(target_path: Path, name: str | None = None, force: bool = False) -> None:
    """Launch interactive TUI for project initialization."""
    from psi.tui.init_tui import InitTUI  # noqa: PLC0415

    app = InitTUI(target_path, name, force)
    app.run()


def list_available_templates() -> None:
    """List all available project templates."""
    console.print("\n[bold]Available Project Templates[/bold]\n")

    for lang, info in LANGUAGE_TEMPLATES.items():
        console.print(f"[cyan]{lang}[/cyan] - {info['description']}")
        if "frameworks" in info:
            for fw, desc in info["frameworks"].items():
                console.print(f"  [green]{fw}[/green]: {desc}")
        if lang == "webdev" and "css_options" in info:
            console.print("  [yellow]CSS options:[/yellow]")
            for css, desc in info["css_options"].items():
                console.print(f"    [magenta]{css}[/magenta]: {desc}")
        console.print()
