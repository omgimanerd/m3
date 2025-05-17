"""Utilities and fixtures for unit testing lockfile.py"""

import json
from pathlib import Path
from typing import Callable

import pytest

from src.config.lockfile import Lockfile


@pytest.fixture
def lockfile_from_path(current_dir) -> Callable[[Path], Lockfile]:
    """Test fixture that returns a helper function to create a Lockfile from a 
    known path."""
    def _lockfile_from_path(relpath):
        fullpath = current_dir / relpath
        with open(fullpath, 'r', encoding='utf-8') as f:
            return Lockfile(**json.load(f), _path=fullpath)
    return _lockfile_from_path
