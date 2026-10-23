"""Filesystem utilities."""

from pathlib import Path
from typing import Any


def ensure_dir(path: Path) -> None:
    """Ensure a directory exists."""
    path.mkdir(parents=True, exist_ok=True)


def get_project_structure(path: Path, max_depth: int = 3) -> dict[str, Any]:
    """Get project structure as a nested dictionary."""
    result: dict[str, Any] = {}
    _scan_directory(path, result, current_depth=0, max_depth=max_depth)
    return result


def _scan_directory(
    path: Path, result: dict[str, Any], current_depth: int, max_depth: int
) -> None:
    """Recursively scan directory."""
    if current_depth >= max_depth:
        return

    try:
        entries = sorted(path.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
    except (PermissionError, OSError):
        return

    for entry in entries:
        # Skip hidden files and common ignore patterns
        if entry.name.startswith(".") or entry.name in {
            "__pycache__", "node_modules", "target", "dist", "build",
            ".venv", "venv", "env", ".git", ".idea", ".vscode",
        }:
            continue

        if entry.is_dir():
            children: dict[str, Any] = {}
            _scan_directory(entry, children, current_depth + 1, max_depth)
            result[entry.name] = {
                "type": "directory",
                "children": children if children else {},
            }
        else:
            try:
                size = entry.stat().st_size
            except OSError:
                size = 0
            result[entry.name] = {
                "type": "file",
                "size": size,
            }
