'''Dataclass wrapper for handling the user's m3.json project configuration'''

from dataclasses import dataclass, make_dataclass
from src.config.project_paths import ProjectPaths

import os
import json

from pathlib import Path
from typing import Optional, Self

CONFIG_FILENAME = 'm3.json'

@dataclass
class Config:
  '''Dataclass container for the user's m3.json project configuration.'''
  # The name of the project
  name: str
  # The version of the project
  version: str
  author: str

  # Paths to assets that m3 can manage relative to the m3.json
  paths: ProjectPaths


  @staticmethod
  def get_config() -> Optional[Self]:
    '''Walk up the directory tree from the current execution context to find
    the a valid m3.json'''
    basepath = Path(os.getcwd())
    while True:
      if str(basepath) == basepath.root:
        return None
      m3_file = basepath / CONFIG_FILENAME
      if m3_file.exists():
        with open(m3_file, 'r', encoding='utf-8') as f:
          try:
            return Config(**json.load(f))
          except json.decoder.JSONDecodeError:
            print(f'Found malformed config file at {m3_file}')
            return None
          except TypeError:
            print(f'Invalid m3.json found at {m3_file}')
            return None
      basepath = basepath.parent
