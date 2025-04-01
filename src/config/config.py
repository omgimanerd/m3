'''Dataclass wrapper for handling the user's m3.json project configuration'''

import json

from pathlib import Path
from typing import Optional, Self

from dataclasses import dataclass

from src.config.project_paths import ProjectPaths
from src.util.enum import Platform
from src.util.paths import walk_up_search


CONFIG_FILENAME = 'm3.json'

@dataclass
class Config:
  '''Dataclass container for the user's m3.json project configuration.'''
  # The name of the project
  name: str
  # The version of the project
  version: str
  authors: list[str]

  # CurseForge or Modrinth
  platform: Platform

  # Paths to assets that m3 can manage relative to the m3.json
  paths: ProjectPaths

  # Path to build the output to.
  output: Path


  @staticmethod
  def get_config() -> Optional[Self]:
    '''Walk up the directory tree from the current execution context to find
    the a valid m3.json'''
    path = walk_up_search(CONFIG_FILENAME)
    with open(path, 'r', encoding='utf-8'):
      try:
        return Config(**json.load(f))
      except json.decoder.JSONDecodeError:
        print(f'Found malformed config file at {path}')
        return None
      except TypeError:
        print(f'Invalid m3.json found at {path}')
        return None

