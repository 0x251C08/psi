"""Tests for Psi."""

from pathlib import Path

from psi.utils.fs import get_project_structure
from psi.utils.dependencies import detect_dependencies
from psi.utils.tools import detect_tool_versions


def test_get_project_structure():
    """Test project structure detection."""
    structure = get_project_structure(Path(__file__).parent.parent)
    assert "src" in structure
    assert structure["src"]["type"] == "directory"
    assert "psi" in structure["src"]["children"]


def test_detect_dependencies():
    """Test dependency detection."""
    deps = detect_dependencies(Path(__file__).parent.parent)
    assert isinstance(deps, list)
    # Should detect Python dependencies
    python_deps = [d for d in deps if d["ecosystem"] == "Python"]
    assert len(python_deps) >= 1


def test_detect_tool_versions():
    """Test tool version detection."""
    tools = detect_tool_versions()
    assert isinstance(tools, list)
    # Should detect at least git, python, and some other tools
    tool_names = [t["name"] for t in tools]
    assert "git" in tool_names
    assert "python" in tool_names