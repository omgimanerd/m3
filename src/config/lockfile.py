"""Dataclass wrapper for handling m3's lockfile"""

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Self

from click import ClickException

from src.util.enum import Platform, Side

LOCKFILE_FILENAME = 'm3.lock.json'


@dataclass
class Lockfile:
    """Dataclass wrapper for handling m3's lockfile"""
    entries: dict[str, LockfileEntry]
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

    def add_entry(self, entry: LockfileEntry):
        """Adds a specified entry to the lockfile object.

        If the object exists, updates the existing entry in the lockfile with a 
        new LockfileEntry object.
        """
        self.entries[entry.name] = entry

    def remove_entry(self, entry: LockfileEntry):
        """Removes a given entry from the lockfile object.

        Returns the removed entry, or None if entry was not found.
        """
        if self.entries.get(entry.name) is not None:
            return self.entries.pop(entry.name)
        return None

    def get_entry(self, entry: LockfileEntry):
        """Gets a specified entry from the lockfile object."""
        return self.entries.get(entry.name)

    def reindex_lockfile_entries(
            self, entries: list[LockfileEntry], f_new_key: Callable
    ):
        """Reindex lockfile entries across all types on a common new key.

        Args:
            entries: the object containing all lockfile entries
            new_key: the new key to reindex lockfile entries by

        Returns:
            dict of reindexed lockfile entries
        """

        try:
            reindexed_dicts = reindex(
                entries, f_new_key
            )
        except Exception as error:
            raise ClickException(
                'Failed to reindex lockfile entries:' + f'{error}') from error
        return reindexed_dicts

    def filter_by_asset_type(self, asset_type: AssetType):
        """Returns a dict containing all entries of a given asset type.

        Args:
            asset_type: The asset type to filter entries by

        Returns:
            A dict keyed by the asset name, containing all entries of the given
            asset type.
        """
        return {name: entry for name, entry in self.entries.items()
                if entry.asset_type == asset_type}
