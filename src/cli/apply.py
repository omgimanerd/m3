"""apply subcommand module"""

import os
import tempfile
from pathlib import Path

import click

from src.config.loader import load_config_and_lockfile
from src.config.lockfile import HASH_ALGS
from src.lib.copy import copy
from src.lib.overwrite import overwrite_dir
from src.util.asset_management import (create_entry_queue, install_assets,
                                       uninstall_assets)
from src.util.hash import hash_asset_dir_multi_hash

R_HELPTEXT = """
Remove assets found in the project asset directories that are not in the
lockfile.
"""


# pylint: disable-next=too-few-public-methods
class Apply:
    """Class for the apply command."""
    @click.command()
    @click.option('-r', '--remove', is_flag=True, help=R_HELPTEXT)
    @staticmethod
    def apply(remove):
        """Applies the lockfile's state to the project assets."""
        config, lockfile = load_config_and_lockfile()

        if config is None or lockfile is None:
            raise click.ClickException('Not an m3 project')
        with tempfile.TemporaryDirectory() as tmpdir:
            for asset_type, path in config.get_asset_paths().items():
                temp_asset_path = Path(tmpdir) / config.paths.get()[asset_type]
                os.makedirs(temp_asset_path, exist_ok=True)
                copy(path, Path(temp_asset_path), include=['*'], exclude=[])

                lockfile_assets_multikey_dict = lockfile.get_assets_by_type(
                    asset_type)
                curr_asset_multikey_dict = hash_asset_dir_multi_hash(
                    temp_asset_path, HASH_ALGS)
                install_queue = create_entry_queue(
                    lockfile_assets_multikey_dict,
                    lockfile_assets_multikey_dict.get_multikey_difference(
                        curr_asset_multikey_dict))

                install_assets(install_queue, temp_asset_path)

                for i in install_queue:
                    click.echo(f'Installed {i.display_name}')

                if remove:
                    uninstall_queue = create_entry_queue(
                        curr_asset_multikey_dict, curr_asset_multikey_dict.
                        get_multikey_difference(lockfile_assets_multikey_dict))
                    uninstall_assets(
                        uninstall_queue, temp_asset_path, click.echo)
            for asset_type, path in config.get_asset_paths().items():
                overwrite_dir(
                    path, (Path(tmpdir) / config.paths.get()[asset_type]))

        click.echo('Applied lockfile state to development directory')
