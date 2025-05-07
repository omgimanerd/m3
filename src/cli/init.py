"""init subcommand module"""

import click
from fire.core import FireError

from src.config.config import Config
from src.util.enum import Platform


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Init:
    @click.command()
    @staticmethod
    def init():
        """Initializes an m3 managed project in the current directory."""
        config = Config.get_config()
        if config is not None:
            raise FireError(
                f'Found an already existing config file: ${config.get_path()}')
        name = click.prompt('Project Name')
        platform = click.prompt(
            'Platform', type=click.Choice(['modrinth', 'curseforge']))
        authors = click.prompt('Authors (comma-separated)')
        print(name, authors, platform)
        config = Config(
            name=name,
            version='',
            platform=Platform(platform),
            authors=authors.split(',')
        )
        config.write()
