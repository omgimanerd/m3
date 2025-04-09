"""list subcommand module"""

import click


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class List:
    @click.command()
    @staticmethod
    def list():
        """List mods currently in lockfile."""
