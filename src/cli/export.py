"""export subcommand module"""


import click

from src.util.click_helpers import CONTEXT_SETTINGS


class Export:
    @click.command(context_settings=CONTEXT_SETTINGS)
    @staticmethod
    def export():
        """Builds the modpack for export."""
