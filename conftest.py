"""Pytest fixtures used by all child directories."""

import json
from pathlib import Path
from typing import Callable

import pytest

# Fixtures defined in modules in this project.
# pylint: disable-next=invalid-name
pytest_plugins = (
    "src.config.config_test_util",
    "src.config.lockfile_test_util"
)


@pytest.fixture
def current_dir(request) -> Path:
    """Test fixture that returns the parent directory of the current test."""
    return request.path.parent


@pytest.fixture
def read_file() -> Callable[[str], str]:
    """Test fixture that returns a function to read the contents of a file."""
    def _read_file(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return _read_file


@pytest.fixture
def read_json_file() -> Callable[[str], str]:
    """Test fixture that returns a function to read the contents of a JSON
    file and return a JSON object."""
    def _read_json_file(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return _read_json_file
