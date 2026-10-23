"""Tests for ${project_name}."""

import pytest
from ${project_name}.core import hello, add


def test_hello():
    assert hello("World") == "Hello, World!"


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


if __name__ == "__main__":
    pytest.main([__file__])