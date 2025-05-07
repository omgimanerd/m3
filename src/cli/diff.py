"""diff subcommand"""

import click


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Diff:
    @click.command()
    @staticmethod
    def diff():
        """Diffs the state of the assets in the project directory with the
        lockfile."""
