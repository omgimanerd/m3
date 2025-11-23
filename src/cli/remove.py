"""uninstall subcommand module"""

import os
import shutil
import tempfile
from pathlib import Path

import click

from src.lib.copy import copy
from src.lib.lockfile_context_manager import M3ContextManager
from src.lib.overwrite import overwrite_dir
from src.util.asset_management import uninstall_asset
from src.util.click import command_with_aliases

INVALID_ASSET_ID_ERROR_MSG = 'Not a valid identifier. Use the m3 internal identifier.'


# pylint: disable-next=missing-class-docstring
class Remove:
    @command_with_aliases('rm', 'uninstall', no_args_is_help=True,
                          short_help='Removes asset from the project.')
    @click.argument('identifier')
    @staticmethod
    def remove(identifier):
        """Removes the specified asset from your file system and lockfile.

        Uses m3's internal identifier to reference the asset to remove.
        """
        with M3ContextManager() as context:
            if context.config is None or context.lockfile is None:
                raise click.ClickException('Not an m3 project')

            try:
                multikey_dict = context.lockfile.create_multikey_dict_for_lockfile()
                if not multikey_dict.is_existing_key(identifier):
                    click.echo(INVALID_ASSET_ID_ERROR_MSG)
                    return

                asset_to_remove = multikey_dict.get(identifier)
                # Use config.get_asset_paths() to get absolute paths
                asset_path = context.config.get_asset_paths()[
                    asset_to_remove.asset_type]

                # Use a temp filesystem and make all changes in the temp fs so that if
                # any errors occur, it does not impact the real filesystem.
                # Makes this command's operation atomic.
                with tempfile.TemporaryDirectory() as tmpdir:
                    # Use config.paths.get() to get relative asset path
                    temp_asset_path = Path(
                        tmpdir) / context.config.paths.get()[asset_to_remove.asset_type]
                    # Create asset dir structure matching real fs in temp fs
                    os.makedirs(temp_asset_path, exist_ok=True)
                    copy(
                        asset_path, Path(temp_asset_path),
                        include=['*'], exclude=[])
                    uninstalled = uninstall_asset(
                        asset_to_remove, temp_asset_path)

                    overwrite_dir(asset_path, temp_asset_path)
                context.lockfile.remove_entry(asset_to_remove)
                click.echo(f'Uninstalled {uninstalled}')
            except ValueError as error:
                raise click.ClickException(error)
            except FileNotFoundError as error:
                raise click.ClickException(
                    'File not found: ' +
                    str(error))
            except (shutil.Error, FileExistsError, OSError) as error:
                raise click.ClickException(
                    'An error occurred when attempting to copy project ' +
                    'state changes: ' + str(error))
