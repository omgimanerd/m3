"""list subcommand module"""

import click

from src.util.click_helpers import CONTEXT_SETTINGS


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class List:
    @click.command(context_settings=CONTEXT_SETTINGS)
    # TODO(a yain): Set this to only accept valid asset types
    @click.option('-t', '--type', help="""Filters the output by asset type.""")
    @staticmethod
    def list():
        """Lists the assets present in the project lockfile configuration.

        Use `m3 diff` to diff it against the project directory contents.
        """
