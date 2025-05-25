"""Dataclass wrapper for handling m3's lockfile"""

import json
import os
from collections.abc import Callable
from dataclasses import field
from pathlib import Path
from typing import Optional, Self, Union

from click.exceptions import ClickException
from pydantic.dataclasses import dataclass

from src.config.lockfile_entry import LockfileEntry
from src.lib.dataclasses import PathField, dataclass_json
from src.util.dicts import reindex
from src.util.enum import AssetType

LOCKFILE_FILENAME = 'm3.lock.json'
HASH_ALGS = ['sha1', 'sha512', 'md5']
DEFAULT_ALG = 'sha512'


@dataclass_json
@dataclass
class Lockfile:
    """Dataclass wrapper for handling m3's lockfile"""
    entries: dict[str, LockfileEntry] = field(default_factory=dict)
    _path: Path = PathField(Path(os.getcwd()) / LOCKFILE_FILENAME)

    @staticmethod
    def create(path: Path) -> Optional[Self]:
        """Factory method that attempts to construct a lockfile dataclass using
        the lockfile in the given directory, returns None if there was no lockfile
        found.

        Args:
          path: The path to attempt to search for a lockfile.

        Returns:
          A Lockfile dataclass instance, or throws an FireError if an invalid
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

    def get_path(self) -> Path:
        """Returns the path of the lockfile."""
        return self._path

    def write(self, path: Optional[Union[Path, str]] = None):
        """Writes the state of this lockfile object to the file.

        Args:
            path: An optional path argument to write the lockfile to, otherwise 
            writes to the default _path member stored in the lockfile.
        """
        with open(path if path is not None else self._path, "w",
                  encoding="utf-8") as f:
            # This is added by the @dataclass_json decorator,
            # pylint: disable-next=no-member
            f.write(self.json())

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
