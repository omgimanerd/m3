"""uninstall subcommand"""

import click

from src.util.click_helpers import command_with_aliases


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Remove:
    @command_with_aliases('rm', 'uninstall', 'u', no_args_is_help=True)
    @click.argument('identifier')
    @staticmethod
    def remove(identifier):
        """Removes the specified asset from your file system and lockfile."""
