"""Helper functions for installing and uninstalling assets."""

import os
from pathlib import Path
from typing import Callable

from src.lib.multikey_dict import MultiKeyDict
from src.util.web import download_file


def install_assets(
        asset_entries: MultiKeyDict, install_queue: set, asset_path: Path,
        echo: Callable):
    """Given a list of assets to install, installs the assets to the asset
    path."""
    for queued_asset in install_queue:
        # TODO: Update to not have to access single key
        asset_entry = asset_entries.get_by_multikey(queued_asset)
        cdn_link = asset_entry.asset.cdn_link
        file_path = asset_path / asset_entry.name
        download_file(cdn_link, file_path)
        echo(f'Installed {asset_entry.name}')


def uninstall_assets(
        asset_entries: MultiKeyDict, uninstall_queue: set, echo: Callable = print):
    """Given a list of assets to uninstall, removes the assets from the asset
    path."""
    for queued_asset in uninstall_queue:
        # TODO: Update to not have to access single key
        asset_file_path = asset_entries.get_by_multikey(queued_asset)

        if os.path.exists(asset_file_path):
            os.remove(asset_file_path)
            echo(f'Uninstalled {asset_file_path.name}')
