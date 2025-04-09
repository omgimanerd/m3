"""add subcommand module"""

import click


# pylint: disable-next=missing-class-docstring
class Add:
    @click.command()
    @staticmethod
    def add():
        """Install a specified mod and add it to the lockfile."""
        click.echo('Installed mod and added to lockfile')
