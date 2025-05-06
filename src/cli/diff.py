"""diff subcommand"""

import click

from src.util.click_helpers import CONTEXT_SETTINGS


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Diff:
    @click.command(context_settings=CONTEXT_SETTINGS)
    @staticmethod
    def diff():
        """Diffs the state of the assets in the project directory with the
        lockfile."""
