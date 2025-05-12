"""Dataclass wrapper for handling m3's lockfile"""


import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Self, Union

from click import ClickException

from src.util.enum import Platform, Side

LOCKFILE_FILENAME = 'm3.lock.json'


@dataclass
class CurseForgeLockfileEntry:
    """Dataclass wrapper for handling CurseForge lockfile entries."""
    mod_id: int
    file_id: int
    cdn_link: str


@dataclass
class ModrinthLockfileEntry:
    """Dataclass wrapper for handling Modrinth lockfile entries."""
    mod_id: int
    slug: str
    cdn_link: str


@dataclass
class LockfileEntry:
    """Dataclass wrapper for handling lockfile entries."""
    name: str
    hash: str
    file_type: Platform
    file_data: Union[CurseForgeLockfileEntry, ModrinthLockfileEntry]
    side: Side = field(default=Side.BOTH)


@dataclass
class Lockfile:
    """Dataclass wrapper for handling m3's lockfile"""
    lockfile_entries: dict[str, LockfileEntry]
    _path: Path

    @staticmethod
    def create(path: Path) -> Optional[Self]:
        """Factory method that attempts to construct a lockfile dataclass using
        the lockfile in the given directory, returns None if there was no lockfile
        found.

        Args:
          path: The path to attempt to search for a lockfile.

        Returns:
          A Lockfile dataclass instance, or throws an ClickError if an invalid
          lockfile was found.
        """
        filepath = path / LOCKFILE_FILENAME
        if not filepath.exists():
            return None
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return Lockfile(**json.load(f), _path=filepath)
        except json.decoder.JSONDecodeError as e:
            raise ClickException(
                f'Found malformed lockfile at {filepath}') from e
        except TypeError as e:
            raise ClickException(
                f'Invalid {LOCKFILE_FILENAME} found at {filepath}') from e

    def write(self):
        """Writes the state of this lockfile object to the file."""
        with open(self._path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self, indent=2))
