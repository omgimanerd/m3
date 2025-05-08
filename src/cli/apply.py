"""apply subcommand module"""

import click

from src.config.config import Config
from src.config.lockfile import Lockfile

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
        # lockfile_entry_manager = LockfileEntryManager(lockfile, config)
        # lockfile_entry_manager.config_hash_maps()
        # lockfile_entry_manager.apply()

        # if remove:
        #     lockfile_entry_manager.prune()
        #     click.echo('Pruned extraneous assets not found in lockfile')
        # click.echo('Applied lockfile state to development directory')
