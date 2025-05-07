"""uninstall subcommand"""

import click


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Remove:
    @click.command()
    @click.argument('identifier')
    @staticmethod
    def remove(identifier):
        """Removes the specified asset from your file system and lockfile."""
