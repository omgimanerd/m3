"""list subcommand module"""

import click


@click.command()
def list_mods():
    """List mods currently in lockfile."""
    # TODO: Alias this command to `list` for user
