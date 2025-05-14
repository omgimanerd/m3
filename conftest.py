"""Pytest fixtures used by all child directories."""

from pathlib import Path

import pytest

# Fixtures defined in modules in this project.
# pylint: disable-next=invalid-name
pytest_plugins = (
    "src.config.config_test_util"
)


@pytest.fixture
def current_dir(request) -> Path:
    """Test fixture that returns the parent directory of the current test."""
    return request.path.parent
