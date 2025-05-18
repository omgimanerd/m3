"""export subcommand module"""


import click

from src.util.click import command_with_aliases


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Export:
    @command_with_aliases('ex')
    @staticmethod
    def export():
        """Builds the modpack for export."""
