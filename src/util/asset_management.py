"""Helper functions for installing and uninstalling assets."""

import os
from pathlib import Path
from typing import Callable

from src.config.lockfile_entry import LockfileEntry
from src.lib.multikey_dict import MultiKeyDict
from src.util.web import download_file


def create_entry_queue(
        lockfile_entries: MultiKeyDict, to_install: set) -> list[LockfileEntry]:
    """Given a lookup dictionary of lockfile entries and a set of asset
    references, return a list of the associated LockfileEntry objects."""
    queue = []
    for queued_asset in to_install:
        queue.append(lockfile_entries.get_by_multikey(queued_asset))
    return queue


def install_asset(
        lockfile_entry: LockfileEntry, asset_path: Path, echo: Callable):
    """Installs the given asset to the asset path."""
    cdn_link = lockfile_entry.asset.cdn_link
    file_path = asset_path / lockfile_entry.name
    download_file(cdn_link, file_path)
    if not lockfile_entry.hash.check_hash(file_path):
        echo(
            'Hash does not match, uninstalling' +
            f'{lockfile_entry.display_name}...')
        uninstall_asset(lockfile_entry, asset_path, echo)
        return
    lockfile_entry.hash.populate_hashes(file_path)
    echo(f'Installed {lockfile_entry.display_name}')


def install_assets(
        lockfile_entries: list[LockfileEntry],
        asset_path: Path, echo: Callable):
    """Given a list of assets to install, installs the assets to the asset
    path."""
    for entry in lockfile_entries:
        install_asset(entry, asset_path, echo)


def uninstall_asset(
        lockfile_entry: LockfileEntry, asset_path: Path, echo: Callable):
    """Uninstalls the given asset located at the given path."""
    file_path = asset_path / lockfile_entry.name
    if os.path.exists(file_path):
        os.remove(file_path)
        echo(f'Uninstalled {lockfile_entry.display_name}')


def uninstall_assets(
        lockfile_entries: list[LockfileEntry],
        asset_path: Path, echo: Callable):
    """Given a list of assets to uninstall, removes the assets from the asset
    path."""
    for entry in lockfile_entries:
        uninstall_asset(entry, asset_path, echo)
