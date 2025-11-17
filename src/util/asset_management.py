"""Helper functions for installing and uninstalling assets."""

import os
from pathlib import Path
from typing import Callable, Union

import requests
from click import ClickException

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
        lockfile_entry: LockfileEntry, asset_path: Path) -> str:
    """Installs the given asset to the asset path."""
    try:
        cdn_link = lockfile_entry.asset.cdn_link
        file_path = asset_path / lockfile_entry.name
        file_hashes = lockfile_entry.hash
        download_file(cdn_link, file_path, file_hashes)
        lockfile_entry.hash.populate_hashes(file_path)
        return lockfile_entry.display_name
    except requests.HTTPError as error:
        raise ClickException(
            f'Error installing {lockfile_entry.display_name}: '
            + f'HTTP error code {error.response.status_code}') from error
    except ValueError as error:
        raise ClickException(
            f'Error installing {lockfile_entry.display_name}: '
            + "Downloaded file hash does not match expected hash") from error


def install_assets(
        lockfile_entries: list[LockfileEntry],
        asset_path: Path) -> list[str]:
    """Given a list of assets to install, installs the assets to the asset
    path."""
    result = []
    for entry in lockfile_entries:
        try:
            result.append(
                install_asset(entry, asset_path))
        except (requests.HTTPError, ValueError) as error:
            raise error
    return result


def uninstall_asset(
        lockfile_entry: Union[LockfileEntry, Path],
        asset_path: Path, echo: Callable) -> str:
    """Uninstalls the given asset located at the given path."""
    if isinstance(lockfile_entry, LockfileEntry):
        file_path = asset_path / lockfile_entry.name
        if os.path.exists(file_path):
            os.remove(file_path)
            echo(f'Uninstalled {lockfile_entry.display_name}')
        return lockfile_entry.display_name

    if os.path.exists(lockfile_entry):
        os.remove(lockfile_entry)
        echo(f'Uninstalled {lockfile_entry.name}')
        return lockfile_entry.name


def uninstall_assets(
        lockfile_entries: list[LockfileEntry],
        asset_path: Path, echo: Callable):
    """Given a list of assets to uninstall, removes the assets from the asset
    path."""
    for entry in lockfile_entries:
        uninstall_asset(entry, asset_path, echo)
