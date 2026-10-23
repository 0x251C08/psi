"""Dependency detection for various ecosystems."""

import json
from pathlib import Path
from typing import Any

import tomli


def detect_dependencies(path: Path) -> list[dict[str, Any]]:
    """Detect project dependencies across ecosystems."""
    dependencies = []

    # Python
    py_deps = _detect_python_deps(path)
    if py_deps:
        dependencies.append(py_deps)

    # Node.js
    node_deps = _detect_node_deps(path)
    if node_deps:
        dependencies.append(node_deps)

    # Rust
    rust_deps = _detect_rust_deps(path)
    if rust_deps:
        dependencies.append(rust_deps)

    # Go
    go_deps = _detect_go_deps(path)
    if go_deps:
        dependencies.append(go_deps)

    # Zig
    zig_deps = _detect_zig_deps(path)
    if zig_deps:
        dependencies.append(zig_deps)

    return dependencies


def _detect_python_deps(path: Path) -> dict[str, Any] | None:
    """Detect Python dependencies."""
    managers: list[dict[str, Any]] = []

    # Check pyproject.toml
    pyproject = path / "pyproject.toml"
    if pyproject.exists():
        try:
            with open(pyproject, "rb") as f:
                data = tomli.load(f)
            deps = data.get("project", {}).get("dependencies", [])
            opt_deps = data.get("project", {}).get("optional-dependencies", {})
            total = len(deps) + sum(len(v) for v in opt_deps.values())
            managers.append({"manager": "pip/uv", "count": total, "file": "pyproject.toml"})
        except Exception:
            pass

    # Check requirements.txt
    req_txt = path / "requirements.txt"
    if req_txt.exists():
        try:
            lines = req_txt.read_text().splitlines()
            count = len([line for line in lines if line.strip() and not line.startswith("#")])
            managers.append({"manager": "pip", "count": count, "file": "requirements.txt"})
        except Exception:
            pass

    # Check poetry.lock
    if (path / "poetry.lock").exists():
        managers.append({"manager": "poetry", "count": "lock file", "file": "poetry.lock"})

    # Check uv.lock
    if (path / "uv.lock").exists():
        managers.append({"manager": "uv", "count": "lock file", "file": "uv.lock"})

    if managers:
        return {
            "ecosystem": "Python",
            "manager": managers[0]["manager"],
            "count": managers[0]["count"],
            "files": [m["file"] for m in managers],
        }
    return None


def _detect_node_deps(path: Path) -> dict[str, Any] | None:
    """Detect Node.js dependencies."""
    package_json = path / "package.json"
    if not package_json.exists():
        return None

    try:
        with open(package_json) as f:
            data = json.load(f)

        deps = data.get("dependencies", {})
        dev_deps = data.get("devDependencies", {})
        total = len(deps) + len(dev_deps)

        # Detect package manager
        if (path / "pnpm-lock.yaml").exists():
            manager = "pnpm"
        elif (path / "yarn.lock").exists():
            manager = "yarn"
        elif (path / "package-lock.json").exists():
            manager = "npm"
        elif (path / "bun.lockb").exists():
            manager = "bun"
        else:
            manager = "npm"

        return {
            "ecosystem": "Node.js",
            "manager": manager,
            "count": total,
            "files": ["package.json"],
        }
    except Exception:
        return None


def _detect_rust_deps(path: Path) -> dict[str, Any] | None:
    """Detect Rust dependencies."""
    cargo_toml = path / "Cargo.toml"
    if not cargo_toml.exists():
        return None

    try:
        with open(cargo_toml, "rb") as f:
            data = tomli.load(f)

        deps = data.get("dependencies", {})
        dev_deps = data.get("dev-dependencies", {})
        total = len(deps) + len(dev_deps)

        return {
            "ecosystem": "Rust",
            "manager": "cargo",
            "count": total,
            "files": ["Cargo.toml", "Cargo.lock"],
        }
    except Exception:
        return None


def _detect_go_deps(path: Path) -> dict[str, Any] | None:
    """Detect Go dependencies."""
    go_mod = path / "go.mod"
    if not go_mod.exists():
        return None

    try:
        content = go_mod.read_text()
        # Count require statements
        in_require = False
        count = 0
        for raw_line in content.splitlines():
            line = raw_line.strip()
            if line.startswith("require ("):
                in_require = True
                continue
            if in_require:
                if line == ")":
                    in_require = False
                elif line and not line.startswith("//"):
                    count += 1
            elif line.startswith("require ") and not line.startswith("require ("):
                count += 1

        return {
            "ecosystem": "Go",
            "manager": "go modules",
            "count": count,
            "files": ["go.mod", "go.sum"],
        }
    except Exception:
        return None


def _detect_zig_deps(path: Path) -> dict[str, Any] | None:
    """Detect Zig dependencies."""
    build_zig = path / "build.zig"
    if not build_zig.exists():
        return None

    # Zig doesn't have a standard dep format yet, just detect presence
    return {
        "ecosystem": "Zig",
        "manager": "zig build",
        "count": 0,
        "files": ["build.zig", "build.zig.zon"],
    }
