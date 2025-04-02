"""Dataclass representing the Curseforge manifest.json file."""

from dataclasses import dataclass


@dataclass
class Files:
  """files subfield."""
  # pylint: disable=invalid-name
  fileID: int
  # pylint: disable=invalid-name
  projectID: int
  required: bool


@dataclass
class Loader:
  """modloaders subfield"""
  id: str
  primary: bool


@dataclass
class Minecraft:
  """minecraft subfield"""
  # pylint: disable=invalid-name
  modLoaders: list[Loader]
  # Minecraft version
  version: str


@dataclass
class Manifest:
  """Parent manifest."""
  author: str
  files: list[Files]

  # pylint: disable=invalid-name
  manifestType: str = 'minecraftModpack'
  # pylint: disable=invalid-name
  manifestVersion: int = 1

  minecraft: Minecraft

  name: str
  overrides: str = 'overrides'
