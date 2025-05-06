"""Utility file with .toml file processing functions."""

import tomllib
from pathlib import Path

from click import ClickException


def read_toml_file(filename: Path) -> dict:
    """Returns a dict containing data from the .toml file.

    Args:
        filename: The path to the .toml file to process

    Returns:
        A dict containing data from the .toml file.
    """
    try:
        with open(filename, 'rb') as f:
            data = tomllib.load(f)
        return data
    except Exception as error:
        raise ClickException('An error occurred while attempting to read the ' +
                             f'toml file {filename}: {error}') from error


def read_dir_of_tomls(dir_: Path) -> list[dict]:
    """Returns a list of dicts containing data from .toml files from the given 
    directory.

    Args:
        dir_: The directory to look for .toml files in

    Returns:
        A list of dicts containing data from .toml files found in the directory.
    """
    try:
        toml_files = []
        for path in dir_.glob('*.toml'):
            print(f'toml path: {path}')
            if path.is_file() and path.suffix == ".toml":
                toml_data = read_toml_file(path)
                toml_files.append(toml_data)
        return toml_files
    except Exception as error:
        raise ClickException('An error occurred while attempting to read the ' +
                             f'toml files in {dir_}: {error}') from error
