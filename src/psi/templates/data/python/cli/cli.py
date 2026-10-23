"""${project_name} - A command-line application."""

import typer
from rich.console import Console

app = typer.Typer(
    name="${project_name}",
    help="A command-line application",
    add_completion=False,
)
console = Console()


@app.command()
def hello(name: str = typer.Argument("World", help="Name to greet")):
    """Say hello."""
    console.print(f"[bold green]Hello, {name}![/bold green]")


@app.command()
def goodbye(name: str = typer.Argument("World", help="Name to say goodbye to")):
    """Say goodbye."""
    console.print(f"[bold red]Goodbye, {name}![/bold red]")


@app.command()
def version():
    """Show version."""
    console.print("[cyan]${project_name} v0.1.0[/cyan]")


if __name__ == "__main__":
    app()