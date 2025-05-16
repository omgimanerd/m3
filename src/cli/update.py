"""update subcommand module"""

import click

from src.util.click_helpers import command_with_aliases


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Update:
    @command_with_aliases('u', no_args_is_help=True)
    @click.argument('identifier')
    @staticmethod
    def update(identifier):
        """Updates the specified asset."""
