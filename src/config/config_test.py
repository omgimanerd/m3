"""Unit testing for config.py"""

import json

from src.config.config import CONFIG_FILENAME, Config, ProjectPaths
from src.util.enum import Platform


def test_config_creation():
    """Tests that creating an empty config results in a valid config."""
    c = Config(name="test-config", version="test")
    assert c == Config(
        name="test-config",
        version="test",
        platform="curseforge",
        authors=[],
        paths=ProjectPaths(
            mods="mods",
            resourcepacks="resourcepacks",
            texturepacks="texturepacks",
            shaderpacks="shaderpacks"
        ),
        output="output",
        client_includes=[],
        client_excludes=[],
        server_includes=[],
        server_excludes=[]
    )


def test_config_read(config_from_path):
    """Tests reading a config from disk."""
    c = config_from_path("testdata/test_m3.json")
    assert c == Config(
        name="test-config",
        version="test",
        platform=Platform.CURSEFORGE,
        authors=["test-author", "test-author2"],
        paths=ProjectPaths(
            mods="mods",
            resourcepacks="custom_subdirectory/resourcepacks",
            texturepacks="texturepacks",
            shaderpacks="shaderpacks",
        ),
        output="output",
        client_includes=["path/to/include_client"],
        client_excludes=["path/to/exclude_client"],
        server_includes=["path/to/include_server"],
        server_excludes=["path/to/exclude_server"],
        _path=c.get_path()
    )


def test_config_write(tmp_path):
    """Tests writing a config to disk."""
    config_path = tmp_path / CONFIG_FILENAME
    c = Config(name="test-config", version="test", _path=config_path)
    c.write()
    with open(config_path, 'r', encoding='utf-8') as f:
        written_json = json.load(f)
    assert written_json == {
        "name": "test-config",
        "version": "test",
        "platform": "curseforge",
        "authors": [],
        "paths": {
            "mods": "mods",
            "resourcepacks": "resourcepacks",
            "texturepacks": "texturepacks",
            "shaderpacks": "shaderpacks"
        },
        "output": "output",
        "client_includes": [],
        "client_excludes": [],
        "server_includes": [],
        "server_excludes": [],
    }
