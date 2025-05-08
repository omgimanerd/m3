"""add subcommand module"""

import click

from src.util.click_helpers import command_with_aliases


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Add:
    @command_with_aliases('a', 'install', 'i', no_args_is_help=True,
                          short_help='Installs assets into the project.')
    @click.argument('identifier')
    @staticmethod
    def add(identifier):
        """Installs the specified asset into your file system and adds it to the
        lockfile.

        If your project is a CurseForge modpack, IDENTIFIER is the CurseForge
        project ID.

        If your project is a Modrinth modpack, IDENTIFIER is the Modrinth
        project slug.
        """
