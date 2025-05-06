"""add subcommand module"""

import click

from src.util.click_helpers import CONTEXT_SETTINGS


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Add:
    @click.command(context_settings=CONTEXT_SETTINGS)
    @click.argument('identifier')
    @staticmethod
    def add():
        """Installs the specified asset into your file system and adds it to the
        lockfile.

        If your project is a CurseForge modpack, IDENTIFIER is the CurseForge
        project ID.

        If your project is a Modrinth modpack, IDENTIFIER is the Modrinth
        project slug.
        """
