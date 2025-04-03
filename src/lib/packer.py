"""Module to handle packing up the configured files into a zipfile."""

import os
import shutil
from fnmatch import fnmatch
from pathlib import Path

from src.config.config import Config

TMP_DIR = '.tmp'


def copy_pack_files(mc_dir: Path, destination: Path,
                    include: list[Path], exclude: list[Path]):
    '''Copies all the include patterns into destination, excluding any files
    that match the exclusion pattern.

    Args:
        mc_dir: the absolute path to the minecraft directory. This serves as
          the root path for all the inclusion and exclusion patterns.
        destination: the absolute path to the destination directory to copy
          files to
        include: list of globs to include
        exclude: list of globs to exclude
    '''
    def ignore_callback(path, names):
        """Argument to shutil.copytree's ignore argument.

        Args:
          path: the path to the directory being visited by copytree
          names: a list of the contents in the directory

        Returns:
          a list containing all the names we should exclude for copying
        """
        # Resolve all paths relative to the minecraft directory
        path = Path(path).relative_to(mc_dir)

        def should_exclude(name):
            """Filter function to check a name against every pattern in the
            list of exclusions."""
            return any(fnmatch(path / name, pattern) for pattern in exclude)
        return list(filter(should_exclude, names))

    def copy_callback(src, dst, *args, **kwargs):
        """Argument to shutil.copytree's copy function, defers the call to
        shutil.copy2."""
        print(f'Copying {src.replace(str(mc_dir), "")}')
        return shutil.copy2(src, dst, *args, **kwargs)

    # Copy over all necessary files for the modpack.
    for pattern in include:
        copy_source = mc_dir / pattern
        copy_target = destination / pattern
        if copy_source.is_dir():
            shutil.copytree(copy_source.absolute(), copy_target.absolute(),
                            ignore=ignore_callback, copy_function=copy_callback,
                            dirs_exist_ok=True)
        else:
            os.makedirs(copy_target.parent, exist_ok=True)
            shutil.copyfile(copy_source.absolute(), copy_target)


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
    client_dir = tmp_dir / 'client'
    copy_pack_files(minecraft_dir, client_dir,
                    config.client_includes, config.client_excludes)

    # Build and write the server output
    server_dir = tmp_dir / 'server'
    copy_pack_files(minecraft_dir, server_dir,
                    config.server_includes, config.server_excludes)
