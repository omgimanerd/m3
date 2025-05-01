"""apply subcommand module"""

import click

from src.config.config import Config
from src.config.lockfile import Lockfile
from src.config.lockfile_entry_manager import LockfileEntryManager


# pylint: disable-next=too-few-public-methods
class Apply:
    """Class for the apply command."""
    @click.command()
    @click.option('-r', '--remove', is_flag=True)
    @staticmethod
    def apply(remove):
        """Apply the current lockfile state to the development directory.

        Installs assets found in the lockfile but not the development directory.
        If the flag `-r` is specified, will remove assets found in the directory 
        but not in the lockfile.
        """
        config = Config.get_config()
        lockfile = Lockfile.create(config.get_path())
        lockfile_entry_manager = LockfileEntryManager(lockfile, config)
        lockfile_entry_manager.config_hash_maps()
        lockfile_entry_manager.apply()

        if remove:
            lockfile_entry_manager.prune()
            click.echo('Pruned extraneous assets not found in lockfile')
        click.echo('Applied lockfile state to development directory')
