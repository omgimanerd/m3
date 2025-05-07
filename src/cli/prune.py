"""prune subcommand module"""

import click


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Prune:
    @click.command()
    @staticmethod
    def prune():
        """Removes assets from the project directory that are not recorded in
        the lockfile.

        Use this command to clean out your project asset directories if you
        installed things using external tools like the Prism launcher.
        """
