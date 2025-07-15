"""diff subcommand module"""

from typing import List, Tuple

import click

from src.config.config import Config
from src.config.loader import load_config_and_lockfile
from src.config.lockfile import HASH_ALGS, Lockfile
from src.util.click import command_with_aliases
from src.util.formatter import CustomOutputFormatter
from src.util.hash import hash_asset_dir_multi_hash


def evaluate_diff(
        config: Config, lockfile: Lockfile) -> Tuple[List[str], List[str]]:
    """Given the config and lockfile of an m3 project, evaluates the diff
    between the lockfile's state and the project's assets."""
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
    return missing_assets, new_assets


# pylint: disable-next=too-few-public-methods
class DiffOutputBuilder:
    """Builds the output for the diff command in a predefined format to
    display."""

    def build_diff_output(
            self, missing_assets: List[str],
            new_assets: List[str]) -> str:
        """Given a list of missing assets and a list of new assets, builds the
        output for the diff command.

        Args:
            missing_assets: The list of missing assets to display
            new_assets: The list of new assets to display

        Returns:
            The output of the diff command as a single string.
        """
        # Display the diff correctly formatted
        formatter = CustomOutputFormatter()
        output = ''
        output += formatter.format(
            '{diff_title:title}', diff_title='Asset Diff')
        output += '\n' + formatter.format(
            '{missing:header}', missing='Lockfile assets missing')
        for asset in missing_assets:
            output += '\n' + formatter.format(
                '{missing_asset:diff_minus}', missing_asset=asset)
        output += '\n' + formatter.format('{separator:separator}', separator='')
        output += '\n' + formatter.format(
            '{new_assets:header}', new_assets='New assets found')
        for asset in new_assets:
            output += '\n' + formatter.format(
                '{new_asset:diff_plus}', new_asset=asset)
        return output


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Diff:
    @command_with_aliases(short_help='Shows the lockfile and current asset diff.')
    @staticmethod
    def diff():
        """Shows the diff between the lockfile's state and the project assets."""
        config, lockfile = load_config_and_lockfile()

        if config is None or lockfile is None:
            raise click.ClickException('Not an m3 project')

        missing_assets, new_assets = evaluate_diff(config, lockfile)

        # Display the diff correctly formatted
        output_builder = DiffOutputBuilder()
        output = output_builder.build_diff_output(missing_assets, new_assets)
        click.echo(output)
