"""Unit testing for config.py"""

import json

import pytest

from src.config.config import CONFIG_FILENAME, Config
from src.util.enum import Platform


@pytest.fixture
def config(tmp_path):
    pass


# TODO: Make tests run pre-commit. CI?
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


def test_config_read(tmp_path):
    pass
