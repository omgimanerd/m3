"""apply subcommand module"""

import click

from src.config.loader import load_config_and_lockfile
from src.config.lockfile import HASH_ALGS
from src.util.asset_management import install_assets, uninstall_assets
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

        for asset_type, path in config.get_asset_paths():
            lockfile_assets_multikey_dict = lockfile.get_assets_by_type(
                asset_type)
            curr_asset_multikey_dict = hash_asset_dir_multi_hash(
                path, HASH_ALGS)
            install_assets(lockfile_assets_multikey_dict,
                           lockfile_assets_multikey_dict.get_multikey_difference(
                               curr_asset_multikey_dict),
                           path, click.echo)

            if remove:
                uninstall_assets(curr_asset_multikey_dict,
                                 curr_asset_multikey_dict.get_multikey_difference(
                                     lockfile_assets_multikey_dict),
                                 click.echo)

        click.echo('Applied lockfile state to development directory')
