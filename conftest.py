"""Pytest fixtures used by all tests in this project."""

import json
import shutil
from collections import OrderedDict
from pathlib import Path
from typing import Callable, Optional

import pytest

from src.util.enum import HashAlg
from src.util.hash import hash_dir

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
def read_file() -> Callable[[Path], str]:
    """Test fixture that returns a function to read the contents of a file."""
    def _read_file(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return _read_file


@pytest.fixture
def read_json_file() -> Callable[[Path], dict]:
    """Test fixture that returns a function to read the contents of a JSON
    file and return a JSON object."""
    def _read_json_file(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return _read_json_file


@pytest.fixture
def copy_test_data_directory(tmp_path) -> Callable[[Path], Path]:
    """Test fixture that returns a function to recursively copy the contents of
    a given source path and return the path to the copied directory."""
    def _copy_test_data_directory(path: Path, dest_path: Path = tmp_path):
        return shutil.copytree(path, dest_path, dirs_exist_ok=True)
    return _copy_test_data_directory


@pytest.fixture
def create_file() -> Callable[[Path], Path]:
    """Test fixture that returns a function to create a file at the given path
    and return the path to the created file."""
    def _create_file(filename: Path, contents: str = None):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(filename)) if contents else f.write(contents)
        return filename
    return _create_file


@pytest.fixture
def dir_not_modified() -> Callable[[Path, str,
                                   Optional[HashAlg]],
                                   bool]:
    """Test fixture that returns a function to check if a given directory has
    been modified based on a hash computed of the initial directory state."""
    def _dir_not_modified(
            dir_: Path, original_dir_hash: str,
            alg: HashAlg = HashAlg.SHA256):
        curr_dir_hash = hash_dir(dir_, alg)
        return curr_dir_hash == original_dir_hash
    return _dir_not_modified


@pytest.fixture
def load_dir() -> Callable[[Path], OrderedDict]:
    """Test fixtures that walks the given directory recursively and loads every
    file in the directory into an ordered dict."""
    def _load_dir(dir_: Path) -> OrderedDict:
        d = OrderedDict()
        for f in sorted(dir_.rglob("*")):
            with open(f, "r", encoding="utf-8") as contents:
                d[f] = contents.read()
        return d
    return _load_dir
