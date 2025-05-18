"""list subcommand module"""

import click

from src.util.click import command_with_aliases


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class List:
    @command_with_aliases('l', 'ls')
    # TODO(a yain): Set this to only accept valid asset types
    @click.option('-t', '--type', help="""Filters the output by asset type.""")
    @staticmethod
    def list(type):
        """Lists the assets present in the project lockfile configuration.

        Use `m3 diff` to diff it against the project directory contents.
        """
