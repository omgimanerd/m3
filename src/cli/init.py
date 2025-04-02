"""init subcommand module"""

from dataclasses import asdict

import click
from fire.core import FireError

from src.config.config import Config
from src.util.enum import Platform


# pylint: disable-next=too-few-public-methods
class Init:
  '''Create an m3 project and set up a config file.'''

  def __init__(self):
    config = Config.get_config()
    if config is not None:
      raise FireError(
        f'Found an already existing config file: ${config.get_path()}')
    name = click.prompt('Project Name')
    platform = click.prompt(
      'Platform', type=click.Choice(['modrinth', 'curseforge']))
    authors = click.prompt('Authors (comma-separated)')
    config = Config(
      name=name,
      version='',
      platform=Platform(platform),
      authors=authors.split(',')
    )
    print(asdict(config, dict_factory=Config.factory))
    # config.write()
