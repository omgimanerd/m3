"""diff subcommand module"""

import click

from src.config.loader import load_config_and_lockfile
from src.config.lockfile import HASH_ALGS
from src.util.click import command_with_aliases
from src.util.hash import hash_asset_dir_multi_hash


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Diff:
    @command_with_aliases(short_help='Shows the lockfile and current asset diff.')
    @staticmethod
    def diff():
        """Shows the diff between the lockfile's state and the project assets."""
        config, lockfile = load_config_and_lockfile()

        if config is None or lockfile is None:
            raise click.ClickException('Not an m3 project')

        missing_assets = []
        new_assets = []
        for asset_type, path in config.get_asset_paths().items():
            lockfile_assets_multikey_dict = lockfile.get_assets_by_type(
                asset_type)
            curr_asset_multikey_dict = hash_asset_dir_multi_hash(
                path, HASH_ALGS)

            missing_asset_set = lockfile_assets_multikey_dict.get_multikey_difference(
                curr_asset_multikey_dict)
            new_asset_set = curr_asset_multikey_dict.get_multikey_difference(
                lockfile_assets_multikey_dict)

            for asset_key in missing_asset_set:
                missing_assets.append(
                    lockfile_assets_multikey_dict.get_by_multikey(asset_key).name)

            for asset_key in new_asset_set:
                new_assets.append(
                    curr_asset_multikey_dict.get_by_multikey(asset_key))

        # Display the diff correctly formatted
        click.echo("=========Asset Diff=========")
        click.echo("ASSETS MISSING FROM LOCKFILE:")
        for asset in missing_assets:
            click.echo(f'- {asset}')
        click.echo("============================")
        click.echo("NEW ASSETS FOUND:")
        for asset in new_assets:
            click.echo(f'+ {asset}')
