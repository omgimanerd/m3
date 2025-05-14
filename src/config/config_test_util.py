"""Utilities and fixtures for unit testing config.py"""

import json
from pathlib import Path
from typing import Callable

import pytest

from src.config.config import Config


@pytest.fixture
def config_from_path(current_dir) -> Callable[[Path], Config]:
    """Test fixture that returns a helper function to create a Config from a
    known path."""
    def _config_from_path(relpath):
        fullpath = current_dir / relpath
        with open(fullpath, 'r', encoding='utf-8') as f:
            return Config(**json.load(f), _path=fullpath)
    return _config_from_path
