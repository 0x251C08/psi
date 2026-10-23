"""Template management for project initialization."""

import shutil
from pathlib import Path
from string import Template
from typing import Any

from psi.utils.fs import ensure_dir

TEMPLATE_DIR = Path(__file__).parent / "data"


def get_template(language: str, framework: str) -> Path | None:
    """Get the template directory for a language/framework combo."""
    template_path = TEMPLATE_DIR / language / framework
    if template_path.exists():
        return template_path
    return None


def list_templates() -> dict[str, list[str]]:
    """List all available templates."""
    result = {}
    if TEMPLATE_DIR.exists():
        for lang_dir in TEMPLATE_DIR.iterdir():
            if lang_dir.is_dir():
                frameworks = [f.name for f in lang_dir.iterdir() if f.is_dir()]
                result[lang_dir.name] = frameworks
    return result


def render_template(template_path: Path, target_path: Path, context: dict[str, Any]) -> None:
    """Render a template directory to target path with context substitution."""
    for src_file in template_path.rglob("*"):
        if src_file.is_file():
            rel_path = src_file.relative_to(template_path)
            # Substitute in path
            dst_path = target_path / Template(str(rel_path)).safe_substitute(context)

            ensure_dir(dst_path.parent)

            # Read and render content
            content = src_file.read_text(encoding="utf-8")
            rendered = Template(content).safe_substitute(context)
            dst_path.write_text(rendered, encoding="utf-8")

            # Preserve executable bit
            if src_file.stat().st_mode & 0o111:
                dst_path.chmod(dst_path.stat().st_mode | 0o111)


def copy_template(template_path: Path, target_path: Path) -> None:
    """Copy template without rendering (for binary files)."""
    shutil.copytree(template_path, target_path, dirs_exist_ok=True)
