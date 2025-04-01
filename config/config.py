'''Dataclass wrapper for handling the user's m3.json project configuration'''

from dataclasses import dataclass

from config.project_paths import ProjectPaths


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
