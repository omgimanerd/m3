"""Utility file with .toml file processing functions."""

import tomllib
from pathlib import Path
from typing import Union


def read_toml_file(filename: Union[str, Path]) -> dict:
    """Returns a dict containing data from the .toml file.

    Args:
        filename: The path to the .toml file to process

    Returns:
        A dict containing data from the .toml file.
    """
    with open(filename, 'rb') as f:
        data = tomllib.load(f)
    return data


def read_toml_dir(dir_: Union[str, Path]) -> list[dict]:
    """Returns a list of dicts containing data from .toml files from the given 
    directory.

    Args:
        dir_: The directory to look for .toml files in

    Returns:
        A list of dicts containing data from .toml files found in the directory.
    """
    toml_files = []
    for path in sorted(Path(dir_).iterdir(), key=lambda p: str(p).lower()):
        if path.is_file() and path.suffix == ".toml":
            toml_data = read_toml_file(path)
            toml_files.append(toml_data)
    return toml_files
