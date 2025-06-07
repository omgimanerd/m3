"""apply subcommand module"""

import click

from src.config.config import Config
from src.config.lockfile import HASH_ALGS, Lockfile
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
        config = Config.get_config()
        lockfile = Lockfile.create(config.get_path())
        print(config)
        print(lockfile)
        lockfile_multikey_dict = lockfile.create_multikey_dict_for_lockfile()
        resolved_asset_paths = config.resolve_asset_paths()

        for path in resolved_asset_paths.values():
            asset_multikey_dict = hash_asset_dir_multi_hash(path, HASH_ALGS)
            lockfile_assets = set(lockfile_multikey_dict.get_multikeys())
            curr_assets = set(asset_multikey_dict.get_multikeys())
            install_queue = lockfile_assets.difference(curr_assets)
            install_assets(lockfile_assets, install_queue, path)

            if remove:
                uninstall_queue = curr_assets.difference(lockfile_assets)
                uninstall_assets(curr_assets, uninstall_queue)

        if remove:
            click.echo('Pruned extraneous assets not found in lockfile')
        click.echo('Applied lockfile state to development directory')
