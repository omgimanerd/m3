"""Module to handle copying over a list of inclusion/exclusion glob patterns."""

import os
import shutil
from fnmatch import fnmatch
from glob import glob
from pathlib import Path
from typing import Callable, Optional


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
    def ignore_callback(path, names):
        """Argument to shutil.copytree's ignore argument.

        Args:
            path: the path to the directory being visited by copytree
            names: a list of the contents in the directory

        Returns:
            a list containing all the names we should exclude for copying
        """
        # Resolve all paths relative to the root directory
        path = Path(path).relative_to(root)

        def should_exclude(name):
            """Filter function to check a name against every pattern in the
            list of exclusions."""
            return any(fnmatch(path / name, pattern) for pattern in exclude)
        return list(filter(should_exclude, names))

    def copy_callback(src, dst, *args, **kwargs):
        """Argument to shutil.copytree's copy function, defers the call to
        shutil.copy2."""
        if callback is not None:
            callback(src.replace(str(root)))
        return shutil.copy2(src, dst, *args, **kwargs)

    for pattern in include:
        # Get all matching files and paths for the inclusion glob.
        for match in glob(pattern, root_dir=root, recursive=True,
                          include_hidden=True):
            source = root / match
            target = dest / match
            if source.is_dir():
                shutil.copytree(source.absolute(), target.absolute(),
                                ignore=ignore_callback, copy_function=copy_callback,
                                dirs_exist_ok=True)
            else:
                os.makedirs(target.parent, exist_ok=True)
                shutil.copyfile(source.absolute(), target)
