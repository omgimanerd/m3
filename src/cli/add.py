"""add subcommand module"""

import click


@click.command()
def add():
    """Install a specified mod to the development directory and add it to the 
    lockfile."""
    click.echo('Installed mod and added to lockfile')
