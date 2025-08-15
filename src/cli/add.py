"""add subcommand module"""

import click

from src.api.apikey import get_api_key
from src.api.wrappers.cf_wrapper import CurseForgeWrapper
from src.config.lockfile_entry import LockfileEntry
from src.lib.lockfile_context_manager import M3ContextManager
from src.util.asset_management import install_asset
from src.util.click import command_with_aliases

INVALID_FILE_ID_ERROR_MSG = 'Not a valid identifier. Currently only support CurseForge modpacks'

# pylint: disable-next=too-few-public-methods, missing-class-docstring


class Add:
    @command_with_aliases('a', 'install', 'i', no_args_is_help=True,
                          short_help='Installs assets into the project.')
    @click.argument('identifier')
    @staticmethod
    def add(identifier):
        """Installs the specified asset into your file system and adds it to the
        lockfile.

        If your project is a CurseForge modpack, IDENTIFIER is the CurseForge
        file ID.

        If your project is a Modrinth modpack, IDENTIFIER is the Modrinth
        project slug.
        """
        with M3ContextManager() as context:
            if context.config is None or context.lockfile is None:
                raise click.ClickException('Not an m3 project')
            if identifier.isdigit():
                try:
                    cf_identifier = int(identifier)
                    cf_client = CurseForgeWrapper(get_api_key())
                    asset_data = cf_client.get_asset_files(
                        [cf_identifier]).data[0]
                    proj_data = cf_client.get_mod(asset_data.modId).data
                    asset_lf_entry = LockfileEntry.create_lockfile_entry_from_resp_obj(
                        proj_data, asset_data)
                    asset_path = context.config.get_asset_paths()[
                        asset_lf_entry.asset_type]
                    install_asset(asset_lf_entry, asset_path, click.echo)
                    context.lockfile.add_entry(asset_lf_entry)
                except ValueError as error:
                    raise click.ClickException(error)
                except FileNotFoundError as error:
                    raise click.ClickException(
                        'An error occurred while checking hash of installed file: ' +
                        error)
            else:
                click.echo(INVALID_FILE_ID_ERROR_MSG)
