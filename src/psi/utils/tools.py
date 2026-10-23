"""Tool version detection."""

import re
import subprocess
from typing import Any

TOOLS = [
    ("git", ["git", "--version"], r"git version (\S+)"),
    ("python", ["python", "--version"], r"Python (\S+)"),
    ("python3", ["python3", "--version"], r"Python (\S+)"),
    ("uv", ["uv", "--version"], r"uv (\S+)"),
    ("pip", ["pip", "--version"], r"pip (\S+)"),
    ("poetry", ["poetry", "--version"], r"Poetry (\S+)"),
    ("node", ["node", "--version"], r"v(\S+)"),
    ("npm", ["npm", "--version"], r"(\S+)"),
    ("pnpm", ["pnpm", "--version"], r"(\S+)"),
    ("yarn", ["yarn", "--version"], r"(\S+)"),
    ("bun", ["bun", "--version"], r"(\S+)"),
    ("cargo", ["cargo", "--version"], r"cargo (\S+)"),
    ("rustc", ["rustc", "--version"], r"rustc (\S+)"),
    ("go", ["go", "version"], r"go version go(\S+)"),
    ("zig", ["zig", "version"], r"(\S+)"),
    ("docker", ["docker", "--version"], r"Docker version (\S+)"),
    ("make", ["make", "--version"], r"GNU Make (\S+)"),
    ("cmake", ["cmake", "--version"], r"cmake version (\S+)"),
    ("clang", ["clang", "--version"], r"clang version (\S+)"),
    ("gcc", ["gcc", "--version"], r"gcc (\S+)"),
]


def detect_tool_versions() -> list[dict[str, Any]]:
    """Detect installed tool versions."""
    results = []

    for name, cmd, pattern in TOOLS:
        version = _get_version(cmd, pattern)
        if version:
            # Find path
            try:
                path_result = subprocess.run(
                    ["which", name] if name != "python3" else ["which", "python3"],
                    capture_output=True,
                    text=True,
                    timeout=2,
                    check=False,
                )
                tool_path = path_result.stdout.strip() if path_result.returncode == 0 else ""
            except Exception:
                tool_path = ""

            results.append({
                "name": name,
                "version": version,
                "path": tool_path,
            })

    return results


def _get_version(cmd: list[str], pattern: str) -> str | None:
    """Get version from command output."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=3, check=False
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            match = re.search(pattern, output)
            if match:
                return match.group(1)
            # Fallback: return first word that looks like a version
            for word in output.split():
                if any(c.isdigit() for c in word) and "." in word:
                    return word
    except Exception:
        pass
    return None
