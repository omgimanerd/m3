"""Unit testing for config.py"""

import json
import os
from pathlib import Path
from typing import Callable

import pytest

from src.config.config import CONFIG_FILENAME, Config, ProjectPaths
from src.util.enum import Platform


@pytest.fixture
def cwd() -> Path:
    return Path(os.getcwd())


@pytest.fixture
def config_from_path() -> Callable[[Path], Config]:
    def _config_from_path(path):
        with open(path, 'r', encoding='utf-8') as f:
            return Config(**json.load(f), _path=path)
    return _config_from_path


def test_config_creation(tmp_path):
    c = Config(name="test-config", version="test")
    # TODO: make a fixture for config testing
    config_path = tmp_path / CONFIG_FILENAME
    c._path = config_path
    c.write()

    with open(config_path) as f:
        written_json = json.load(f)

    assert written_json == {
        'name': 'test-config',
        'version': 'test',
        'platform': 'curseforge',
        'authors': [],
        'paths': {
            'mods': 'mods',
            'resourcepacks': 'resourcepacks',
            'texturepacks': 'texturepacks',
            'shaderpacks': 'shaderpacks'
        },
        'output': 'output',
        'client_includes': [],
        'client_excludes': [],
        'server_includes': [],
        'server_excludes': []
    }


def test_config_read(cwd, config_from_path):
    c = config_from_path(cwd / 'testdata/test_m3.json')
    assert c == Config(
        name="test-config",
        version="test",
        platform="curseforge",
        authors=["test-author", "test-author2"],
        paths=ProjectPaths(
            mods="mods",
            resourcepacks="custom_subdirectory/resourcepacks",
            texturepacks="texturepacks",
            shaderpacks="shaderpacks",
        ),
        output="output",
        client_includes=[
            Path("path/to/include_client")
        ],
        client_excludes=[
            Path("path/to/exclude_client")
        ],
        server_includes=[
            Path("path/to/include_server")
        ],
        server_excludes=[
            Path("path/to/exclude_server")
        ],
        _path=cwd / 'testdata/test_m3.json'
    )
