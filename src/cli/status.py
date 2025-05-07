"""diff subcommand"""

import click


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Status:
    @click.command()
    @staticmethod
    def status():
        """Displays the state of the assets in the project directory any diffs
        with the lockfile."""
