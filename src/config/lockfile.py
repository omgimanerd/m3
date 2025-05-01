"""Dataclass wrapper for handling m3's lockfile"""


import hashlib
import json
import os
import tomllib
from collections.abc import Callable
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
    version_id: str
    cdn_link: str


@dataclass
class HashEntry:
    """Dataclass wrapper for handling file hashes of different hash algorithms."""
    sha1: str
    sha512: str
    md5: str


@dataclass
class LockfileEntry:
    """Dataclass wrapper for handling lockfile entries."""
    name: str
    hash: HashEntry
    file_name: str
    file_type: Platform
    file_data: Union[CurseForgeLockfileEntry, ModrinthLockfileEntry]
    side: Side = field(default=Side.BOTH)


@dataclass
class LockfileEntries:
    """Dataclass wrapper for handling different types of lockfile entries.

    Indexed by a unique name as a string.
    """
    mods: dict[str, LockfileEntry] = field(default={})
    resoucepacks: dict[str, LockfileEntry] = field(default={})
    texturepacks: dict[str, LockfileEntry] = field(default={})
    shaderpacks: dict[str, LockfileEntry] = field(default={})


@dataclass
class Lockfile:
    """Dataclass wrapper for handling m3's lockfile"""
    lockfile_entries: LockfileEntries
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

    def add_entry(self, entry: LockfileEntry, entry_type: Asset):
        """Adds a specified entry to the lockfile object."""
        if self.get_entry(entry, entry_type) is None:
            if type is Asset.MOD:
                self.lockfile_entries.mods[entry.name] = entry
            elif type is Asset.RESOURCE:
                self.lockfile_entries.resoucepacks[entry.name] = entry
            elif type is Asset.TEXTURE:
                self.lockfile_entries.texturepacks[entry.name] = entry
            else:
                self.lockfile_entries.shaderpacks[entry.name] = entry
        else:
            raise ClickException(f'{entry_type} {entry.name} ' +
                                 'already exists in lockfile')

    def remove_entry(self, entry: LockfileEntry, entry_type: Asset):
        """Removes a given entry from the lockfile object.

        Returns the removed entry, or None if entry was not found.
        """
        if self.get_entry(entry, entry_type) is not None:
            if type is Asset.MOD:
                removed = self.lockfile_entries.mods.pop(entry.name)
            elif type is Asset.RESOURCE:
                removed = self.lockfile_entries.resoucepacks.pop(entry.name)
            elif type is Asset.TEXTURE:
                removed = self.lockfile_entries.texturepacks.pop(entry.name)
            else:
                removed = self.lockfile_entries.shaderpacks.pop(entry.name)

            return removed
        return None

    def update_entry(self, entry: LockfileEntry, entry_type: Asset):
        """Updates an existing entry in the lockfile with a new LockfileEntry 
        object.

        If the object does not exist, adds it to the lockfile as a new entry.
        """
        if self.get_entry(entry, entry_type) is not None:
            if type is Asset.MOD:
                self.lockfile_entries.mods[entry.name] = entry
            elif type is Asset.RESOURCE:
                self.lockfile_entries.resoucepacks[entry.name] = entry
            elif type is Asset.TEXTURE:
                self.lockfile_entries.texturepacks[entry.name] = entry
            else:
                self.lockfile_entries.shaderpacks[entry.name] = entry
        else:
            self.add_entry(entry, entry_type)

    def get_entry(self, entry: LockfileEntry, entry_type: Asset):
        """Gets a specified entry from the lockfile object."""
        if entry_type is Asset.MOD:
            return self.lockfile_entries.mods.get(entry.name)
        if entry_type is Asset.RESOURCE:
            return self.lockfile_entries.resoucepacks.get(entry.name)
        if entry_type is Asset.TEXTURE:
            return self.lockfile_entries.texturepacks.get(entry.name)
        return self.lockfile_entries.shaderpacks.get(entry.name)

    def reindex_lockfile_entries(
            self, lockfile_entries: LockfileEntries, f_new_key: Callable
    ):
        """Reindex lockfile entries across all types on a common new key.

        Args:
            lockfile_entries: the object containing all lockfile entry types
            new_key: the new key to reindex lockfile entries by

        Returns:
            dict of reindexed lockfile entries, indexed by type
        """

        try:
            reindexed_dicts = {
                'mod_entries': reindex(
                    lockfile_entries.mod_entries, f_new_key
                ),
                'resource_entries': reindex(
                    lockfile_entries.resouce_entries, f_new_key
                ),
                'texture_entries': reindex(
                    lockfile_entries.texture_entries, f_new_key
                ),
                'shader_entries': reindex(
                    lockfile_entries.shader_entries, f_new_key
                )
            }
        except Exception as error:
            raise ClickException(
                'Failed to reindex lockfile entries:' + f'{error}') from error
        return reindexed_dicts


class LockfileContextManager():
    """Context manager for m3 lockfile."""

    def __init__(self, filename: str, mode: str):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding='utf-8')
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.file.close()
