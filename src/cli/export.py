"""export subcommand module"""


import click


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Export:
    @click.command()
    @staticmethod
    def export():
        """Builds the modpack for export."""
