"""Module to handle packing up the configured files into a zipfile."""

import os
import shutil
from fnmatch import fnmatch
from glob import glob
from pathlib import Path

from src.config.config import Config

TMP_DIR = ".tmp"


def copy_files(root: Path, dest: Path, include: list[Path],
               exclude: list[Path]):
    """Copies all of the include patterns rooted at root into destination,
    excluding any files that match the exclusion pattern.

    Args:
        root: the path to the root directory that all the inclusion and
            exclusion patterns will search from
        dest: the path to the copy matching patterns to
        include: a list of globs to include
        exclude: a list of globs to exclude
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
        print(f"Copying {src.replace(str(root), "")}")
        return shutil.copy2(src, dst, *args, **kwargs)

    for pattern in include:
        for match in glob(pattern, root_dir=root, recursive=True):
            source = Path(root / match)
            target = Path(dest / match)
            if source.is_dir():
                shutil.copytree(source.absolute(), target.absolute(),
                                ignore=ignore_callback, copy_function=copy_callback,
                                dirs_exist_ok=True)
            else:
                os.makedirs(target.parent, exist_ok=True)
                shutil.copyfile(source.absolute(), target)


def export(config: Config):
    """Handles exporting the client and server pack to the designated output
    directory as specified by the given config, using the provided inclusion
    and exclusion globs.

    Args:
      config: the m3 configuration to read
    """
    minecraft_dir = config.get_path().parent
    tmp_dir = config.output / TMP_DIR

    # Build and write the client output
    client_dir = tmp_dir / "client"
    copy_files(minecraft_dir, client_dir,
               config.client_includes, config.client_excludes)

    # Build and write the server output
    server_dir = tmp_dir / "server"
    copy_files(minecraft_dir, server_dir,
               config.server_includes, config.server_excludes)
