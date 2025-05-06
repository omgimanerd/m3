"""uninstall subcommand"""

import click

from src.util.click_helpers import CONTEXT_SETTINGS


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Remove:
    @click.command(context_settings=CONTEXT_SETTINGS)
    @click.argument('identifier')
    @staticmethod
    def remove():
        """Removes the specified asset from your file system and lockfile."""
