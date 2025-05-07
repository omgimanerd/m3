"""add subcommand module"""

import click


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Add:
    @click.command()
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
