"""Codebase inspection logic."""

import json
import subprocess
from pathlib import Path
from typing import Any

import tomli
from git import InvalidGitRepositoryError, Repo

from psi.utils.dependencies import detect_dependencies
from psi.utils.fs import get_project_structure
from psi.utils.tools import detect_tool_versions


def inspect_codebase(path: Path, verbose: bool = False) -> dict[str, Any]:
    """Inspect a codebase and return structured information."""
    path = path.resolve()

    result = {
        "project": _get_project_info(path),
        "git": _get_git_info(path),
        "dependencies": detect_dependencies(path),
        "tools": detect_tool_versions(),
        "structure": get_project_structure(path, max_depth=3 if not verbose else 5),
    }

    return result


def _get_project_info(path: Path) -> dict[str, Any]:
    """Extract basic project information."""
    name = path.name

    # Try to get name from various config files
    for config_file in ["pyproject.toml", "package.json", "Cargo.toml", "go.mod", "build.zig"]:
        config_path = path / config_file
        if config_path.exists():
            try:
                if config_file == "pyproject.toml":
                    with open(config_path, "rb") as f:
                        data = tomli.load(f)
                        name = data.get("project", {}).get("name", name)
                elif config_file == "package.json":
                    with open(config_path) as f:
                        data = json.load(f)
                        name = data.get("name", name)
                elif config_file == "Cargo.toml":
                    with open(config_path, "rb") as f:
                        data = tomli.load(f)
                        name = data.get("package", {}).get("name", name)
                elif config_file == "go.mod":
                    with open(config_path) as f:
                        first_line = f.readline().strip()
                        if first_line.startswith("module "):
                            name = first_line.split(" ")[1].split("/")[-1]
                elif config_file == "build.zig":
                    # Zig projects often use directory name
                    pass
            except Exception:
                pass
            break

    return {
        "name": name,
        "path": str(path),
    }


def _get_git_info(path: Path) -> dict[str, Any]:
    """Extract git repository information."""
    try:
        repo = Repo(path, search_parent_directories=True)
        git_dir = repo.git_dir

        # Get current branch
        try:
            branch = repo.active_branch.name
        except TypeError:
            branch = "detached HEAD"

        # Get current commit
        commit = repo.head.commit.hexsha

        # Get status
        status = "clean"
        if repo.is_dirty():
            status = "dirty"
        elif repo.untracked_files:
            status = "untracked files"

        # Get remotes
        remotes = [remote.name for remote in repo.remotes]

        return {
            "is_repo": True,
            "git_dir": str(git_dir),
            "branch": branch,
            "commit": commit,
            "status": status,
            "remotes": remotes,
        }
    except InvalidGitRepositoryError:
        return {
            "is_repo": False,
            "git_dir": None,
            "branch": None,
            "commit": None,
            "status": None,
            "remotes": [],
        }
    except Exception as e:
        return {
            "is_repo": False,
            "error": str(e),
        }


def _run_command(cmd: list[str]) -> tuple[int, str, str]:
    """Run a command and return (exit_code, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return -1, "", ""
