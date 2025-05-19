"""Module to handle copying over a list of inclusion/exclusion glob patterns."""

import shutil
from pathlib import Path
from typing import Callable, Optional


def _is_excluded(path: Path, exclude: list[Path]):
    """Returns True if path matches any pattern in exclude."""
    for pattern in exclude:
        if path.full_match(pattern):
            return True
    return False


def copy(root: Path, dest: Path, include: list[Path], exclude: list[Path],
         callback: Optional[Callable[[str], None]] = None):
    """Copies all of the include patterns rooted at root into destination,
    excluding any files that match the exclusion pattern.

    Args:
        root: the path to the root directory that all the inclusion and
            exclusion patterns will search from
        dest: the path to the copy matching patterns to
        include: a list of globs to include
        exclude: a list of globs to exclude
        callback: an optional callback that will be invoked with each file that
            is copied, can be used to provide logging or other functionality
    """
    for pattern in include:
        for path in root.glob(pattern):
            relative = path.relative_to(root)
            if path.is_dir():
                continue
            if _is_excluded(relative, exclude):
                continue
            if callback is not None:
                callback(path)
            # Generate the full destination path by taking the pattern match
            # relative to the root.
            dest_file = dest / relative
            if not dest_file.parent.exists():
                dest_file.parent.mkdir(exist_ok=True)
            shutil.copy(path, dest / path.relative_to(root))
