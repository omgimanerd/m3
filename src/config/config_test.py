"""Unit testing for config.py"""

import json
from pathlib import Path

from src.config.config import CONFIG_FILENAME, Config, ProjectPaths
from src.util.enum import Platform


def test_config_creation():
    """Tests that creating an empty config results in a valid config."""
    c = Config(name="test-config", version="test")
    assert c == Config(
        name="test-config",
        version="test",
        platform=Platform.CURSEFORGE,
        authors=[],
        paths=ProjectPaths(
            mods=Path("mods"),
            resourcepacks=Path("resourcepacks"),
            texturepacks=Path("texturepacks"),
            shaderpacks=Path("shaderpacks"),
        ),
        output=Path("output"),
        client_includes=[],
        client_excludes=[],
        server_includes=[],
        server_excludes=[]
    )


def test_config_read(tmp_path, config_from_path):
    """Tests reading a config from disk."""
    c = config_from_path("testdata/test_m3.json")
    assert c == Config(
        name="test-config",
        version="test",
        platform=Platform.CURSEFORGE,
        authors=["test-author", "test-author2"],
        paths=ProjectPaths(
            mods=Path("mods"),
            resourcepacks=Path("custom_subdirectory/resourcepacks"),
            texturepacks=Path("texturepacks"),
            shaderpacks=Path("shaderpacks"),
        ),
        output=Path("output"),
        client_includes=[Path("path/to/include_client")],
        client_excludes=[Path("path/to/exclude_client")],
        server_includes=[Path("path/to/include_server")],
        server_excludes=[Path("path/to/exclude_server")],
        _path=c.get_path()
    )
    # Write the config back to a temporary directory and compare the contents.


def test_config_write_read(tmp_path, config_from_path):
    """Tests writing a config to disk results in an identical JSON."""
    config_path = tmp_path / CONFIG_FILENAME
    config = Config(
        name="test-config-write",
        version="test",
        platform=Platform.MODRINTH,
        authors=["author1", "author2"],
        paths=ProjectPaths(
            mods=Path("mods"),
            resourcepacks=Path("subdir/resourcepacks"),
            texturepacks=Path("texturepacks"),
            shaderpacks=Path("shaderpacks"),
        ),
        output=Path("output"),
        client_includes=[
            Path("kubejs"),
        ],
        client_excludes=[
            Path("*.gitignore")
        ],
        server_includes=[
            Path("kubejs"),
        ],
        server_excludes=[
            Path("*.gitignore")
        ],
        _path=config_path
    )
    config.write()
    with open(config_path, "r", encoding="utf-8") as f:
        written_json = json.load(f)
    assert written_json == {
        "name": "test-config-write",
        "version": "test",
        "platform": "modrinth",
        "authors": ["author1", "author2"],
        "paths": {
            "mods": "mods",
            "resourcepacks": "subdir/resourcepacks",
            "texturepacks": "texturepacks",
            "shaderpacks": "shaderpacks"
        },
        "output": "output",
        "client_includes": ["kubejs"],
        "client_excludes": ["*.gitignore"],
        "server_includes": ["kubejs"],
        "server_excludes": ["*.gitignore"],
    }
    # Check that reading back the same config results in the same object.
    written_config = config_from_path(config_path)
    assert config == written_config
