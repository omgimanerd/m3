"""Pytest fixtures used by all tests in this project."""

import json
import os
import shutil
import tempfile
from collections import OrderedDict
from pathlib import Path
from typing import Callable

import pytest

from src.config.config import Config

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
def setup_asset_dir(tmp_path) -> Callable[[Path], Path]:
    """Test fixture that returns a function to set up a default asset directory
    structure for testing in the given root path and return the path to the root
    of the structure."""
    def _setup_asset_dir(config: Config, dest_path: Path = tmp_path):
        for _, asset_path in config.paths.get().items():
            os.makedirs(dest_path / asset_path, exist_ok=True)
        return dest_path
    return _setup_asset_dir


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
        os.makedirs(filename.parent, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(contents if contents else str(filename))
        return filename
    return _create_file


@pytest.fixture
def load_dir() -> Callable[[Path], OrderedDict]:
    """Test fixtures that walks the given directory recursively and loads every
    file in the directory into an ordered dict."""
    def _load_dir(dir_: Path) -> OrderedDict:
        d = OrderedDict()
        for f in sorted(dir_.rglob("*")):
            try:
                if Path(f).is_file():
                    with open(f, "r", encoding="utf-8") as contents:
                        d[f] = contents.read()
            except UnicodeDecodeError:
                continue
        return d
    return _load_dir


@pytest.fixture
def create_tmpdir() -> Callable[[Path], Path]:
    """Test fixture that creates a temporary directory with the specified path."""
    def _create_tmpdir(dir_: Path) -> Path:
        return os.makedirs(dir_, exist_ok=True)
    return _create_tmpdir
