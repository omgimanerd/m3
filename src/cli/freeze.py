"""freeze subcommand module"""

import click

from src.util.click_helpers import CONTEXT_SETTINGS


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Freeze:
    @click.command(context_settings=CONTEXT_SETTINGS)
    @staticmethod
    def freeze():
        """Saves the state of the project's current assets into the lockfile.

        Use this command if you have installed assets with external tools like
        the Prism launcher.
        """
