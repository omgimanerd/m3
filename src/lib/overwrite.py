"""Module to handle overwriting a given directory with contents from a source directory."""

import shutil
from pathlib import Path


def _delete_directory(path: Path):
    """Deletes the given directory if it exists."""
    try:
        shutil.rmtree(path)
    except FileNotFoundError as e:
        raise e


def overwrite_dir(
        dest: Path, src: Path):
    """Overwrites and replaces the contents of the destination directory with
    the contents from the source directory.

    Args:
        dest: the directory to overwrite the contents of
        src: the directory containing the contents to overwrite the dest with
    """
    try:
        _delete_directory(dest)
        shutil.copytree(src, dest)
    except shutil.Error as error:
        err_msg = "Errors occurred during copytree operation:\n"
        for err_info in error.args[0]:
            s, d, msg = err_info
            err_msg += f"Failed to copy '{s}' to '{d}': {msg}\n"
        raise OSError(err_msg) from error
    except FileExistsError as error:
        raise FileExistsError(
            f"Error: Destination directory '{dest}' already exists") from error
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Error: Source directory '{src}' not found") from error
    except OSError as error:
        raise error
