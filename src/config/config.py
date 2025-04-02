"""Dataclass wrapper for handling the user's m3 project configuration"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Self

from fire.core import FireError

from src.util.enum import Platform
from src.util.paths import walk_up_search

CONFIG_FILENAME = 'm3.json'


@dataclass
class ProjectPaths:
  """Dataclass for representing paths to the directories for assets that m3
  should manage."""
  mods: Path = Path('mods')
  resourcepacks: Path = Path('resourcepacks')
  texturepacks: Path = Path('texturepacks')
  shaderpacks: Path = Path('shaderpacks')


@dataclass
class Config:
  """Dataclass container for the user's m3.json project configuration."""
  # The name of the project
  name: str = None
  # The version of the project
  version: str = None
  authors: list[str] = None

  # CurseForge or Modrinth
  platform: Platform = None

  # Paths to assets that m3 can manage relative to the m3.json
  paths: ProjectPaths = None

  # Path to build the output to.
  output: Path = None

  # The path of the config file this object represents.
  _path: Path = None

  @staticmethod
  def factory(config):
    """Dict factory method for dataclasses.asdict()"""
    return {k: v for (k, v) in config if v is not None}

  @staticmethod
  def get_config() -> Optional[Self]:
    """Walk up the directory tree from the current execution context to find
    the a valid m3.json"""
    path = walk_up_search(CONFIG_FILENAME)
    if path is None:
      return None
    # Attempt to open and parse it if one is found.
    with open(path, 'r', encoding='utf-8') as f:
      try:
        return Config(**json.load(f), _path=path)
      except json.decoder.JSONDecodeError as exc:
        raise FireError(
            f'Found malformed config file at {path}') from exc
      except TypeError as exc:
        raise FireError(
            f'Invalid {CONFIG_FILENAME} found at {path}') from exc

  def get_path(self) -> Path:
    """Returns the path of the config file."""
    return self._path

  def write(self):
    """Writes the state of this config object to the config file."""
    with open(self._path, 'w', encoding='utf-8') as f:
      f.write(json.dumps(self, indent=2))
