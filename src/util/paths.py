"""Utility file with path manipulation functions."""

from pathlib import Path
from typing import Optional


def walk_up_search(filename: str) -> Optional[Path]:
    """Walks up from the current execution context looking for a given filename.

    Args:
        filename: the filename to search for in parent directories.

    Returns:
        The path to the file, if found, or None.
    """
    current = Path.cwd()
    while True:
        if str(current) == current.root:
            return None
        filepath = current / filename
        if filepath.exists():
            return filepath
        current = current.parent


def resolve_relative_path(start: Path, path: Path) -> Optional[Path]:
    """Takes a starting point and attempts to resolve a relative path.

    Args:
        start: an absolute path to start from.
        path: a relative path to resolve.

    Returns:
        An absolute path for the given relative path if valid, or None.
    """
    resolved = start / path

    return resolved if resolved.exists() else None
