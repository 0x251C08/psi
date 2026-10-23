"""Main CLI entry point for Psi."""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

from psi.commands.init import init_project, init_project_tui
from psi.commands.inspect import inspect_codebase

app = typer.Typer(
    name="psi",
    help="Developer quality-of-life tool for codebase inspection and project initialization",
    add_completion=False,
    rich_markup_mode="rich",
)
console = Console()


@app.command()
def inspect(
    path: Annotated[
        Path,
        typer.Argument(
            help="Path to the codebase/project to inspect",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = Path.cwd(),
    json_output: Annotated[
        bool,
        typer.Option("--json", "-j", help="Output results as JSON for automation"),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Show detailed information"),
    ] = False,
) -> None:
    """Inspect a codebase: git repo, dependencies, tool versions, and project structure."""
    result = inspect_codebase(path, verbose=verbose)

    if json_output:
        console.print_json(data=result)
    else:
        _display_inspect_result(result, console)


def _display_inspect_result(result: dict, console: Console) -> None:
    """Display inspection results in a rich format."""
    # Project info
    console.print(f"\n[bold cyan]Project:[/bold cyan] {result['project']['name']}")
    console.print(f"[bold cyan]Path:[/bold cyan] {result['project']['path']}")

    # Git info
    if result["git"]["is_repo"]:
        console.print("\n[bold green]Git Repository[/bold green]")
        git_table = Table(show_header=False, box=None)
        git_table.add_column("Key", style="dim")
        git_table.add_column("Value")
        git_table.add_row("Branch", result["git"]["branch"])
        git_table.add_row("Commit", result["git"]["commit"][:12])
        git_table.add_row("Status", result["git"]["status"])
        git_table.add_row("Remotes", ", ".join(result["git"]["remotes"]) or "none")
        console.print(git_table)
    else:
        console.print("\n[yellow]Not a git repository[/yellow]")

    # Dependencies
    if result["dependencies"]:
        console.print("\n[bold green]Dependencies[/bold green]")
        dep_table = Table()
        dep_table.add_column("Language/Ecosystem", style="cyan")
        dep_table.add_column("Manager", style="magenta")
        dep_table.add_column("Dependencies", style="green")
        for dep in result["dependencies"]:
            dep_table.add_row(dep["ecosystem"], dep["manager"], str(dep["count"]))
        console.print(dep_table)

    # Tool versions
    if result["tools"]:
        console.print("\n[bold green]Tool Versions[/bold green]")
        tool_table = Table()
        tool_table.add_column("Tool", style="cyan")
        tool_table.add_column("Version", style="green")
        tool_table.add_column("Path", style="dim")
        for tool in result["tools"]:
            tool_table.add_row(tool["name"], tool["version"], tool.get("path", ""))
        console.print(tool_table)

    # Project structure
    if result["structure"]:
        console.print("\n[bold green]Project Structure[/bold green]")
        tree = Tree(f"[bold]{result['project']['name']}[/bold]")
        _build_tree(tree, result["structure"])
        console.print(tree)


def _build_tree(tree: Tree, structure: dict, prefix: str = "") -> None:
    """Recursively build a rich tree from structure dict."""
    for name, info in sorted(structure.items()):
        if info.get("type") == "directory":
            branch = tree.add(f"[blue]{name}/[/blue]")
            if "children" in info:
                _build_tree(branch, info["children"])
        else:
            size = info.get("size", 0)
            if size > 0:
                tree.add(f"[green]{name}[/green] [dim]({_format_size(size)})[/dim]")
            else:
                tree.add(f"[green]{name}[/green]")


def _format_size(size: int) -> str:
    """Format file size in human-readable format."""
    KB = 1024
    size_float: float = size
    for unit in ["B", "KB", "MB", "GB"]:
        if size_float < KB:
            return f"{size_float:.1f}{unit}"
        size_float /= KB
    return f"{size_float:.1f}TB"


@app.command()
def init(
    language: Annotated[
        str | None,
        typer.Argument(help="Programming language or project type (python, zig, webdev, etc.)"),
    ] = None,
    name: Annotated[
        str | None,
        typer.Option("--name", "-n", help="Project name (defaults to directory name)"),
    ] = None,
    path: Annotated[
        Path | None,
        typer.Option("--path", "-p", help="Target directory (defaults to current directory)"),
    ] = None,
    interactive: Annotated[
        bool,
        typer.Option("--interactive", "-i", help="Launch interactive TUI for project setup"),
    ] = False,
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Overwrite existing files"),
    ] = False,
) -> None:
    """Initialize a new project in the specified language.

    Supported languages: python, zig, rust, go, node, webdev
    Webdev options: html, css (tailwind, vanilla, bootstrap),
    js (vanilla, typescript, react, vue, svelte)
    Python frameworks: flask, fastapi, django, cli
    """
    target_path = path or Path.cwd()

    if interactive or language is None:
        init_project_tui(target_path, name, force)
    else:
        init_project(language, target_path, name, force)


if __name__ == "__main__":
    app()
