"""Dataclass wrapper for handling the user"s m3 project configuration"""

import json
import os
from dataclasses import field
from pathlib import Path
from typing import Optional, Self, Union

from click import ClickException
from pydantic.dataclasses import dataclass

from src.lib.dataclasses import PathField, dataclass_json, get_field_names
from src.util.enum import Platform
from src.util.paths import resolve_relative_path, walk_up_search

CONFIG_FILENAME = "m3.json"


@dataclass_json
@dataclass
class ProjectPaths:
    """Dataclass for representing paths to the directories for assets that m3
    should manage."""
    mods: Path = PathField("mods")
    resourcepacks: Path = PathField("resourcepacks")
    texturepacks: Path = PathField("texturepacks")
    shaderpacks: Path = PathField("shaderpacks")


@dataclass_json
@dataclass
# pylint: disable-next=too-many-instance-attributes
class Config:
    """Dataclass container for the user's m3.json project configuration. In a
    development modpack setup, this should be located in the minecraft/
    directory."""
    # The name of the project
    name: str
    # The version of the project
    version: str = ""
    # CurseForge or Modrinth
    platform: Platform = field(default=Platform.CURSEFORGE)
    # Authors of the project
    authors: list[str] = field(default_factory=list)

    # Paths to assets that m3 can manage relative to the config file itself
    paths: ProjectPaths = field(default_factory=ProjectPaths)

    # Path to put built/exported output to.
    output: Path = PathField("output")

    # List of glob matchers for files to include/exclude in the client modpack
    client_includes: list[Path] = field(default_factory=list)
    client_excludes: list[Path] = field(default_factory=list)
    # List of glob matchers for files to include/exclude in the server modpack
    server_includes: list[Path] = field(default_factory=list)
    server_excludes: list[Path] = field(default_factory=list)

    # The path of the config file this object represents.
    _path: Path = PathField(Path(os.getcwd()) / CONFIG_FILENAME)

    @staticmethod
    def from_json(obj: dict) -> Self:
        """Attempts to deserialize the given json dict into a Config instance.
        """
        try:
            return Config(**obj)
        except json.decoder.JSONDecodeError as exc:
            raise ClickException(
                "Could not deserialize JSON into a Config instance") from exc

    @staticmethod
    # TODO: this should take a default path arg to look in the directory for
    # a config file. Otherwise it will do a directory walk.
    def get_config() -> Optional[Self]:
        """Walk up the directory tree from the current execution context to find
        the a valid m3.json"""
        path = walk_up_search(CONFIG_FILENAME)
        if path is None:
            return None
        # Attempt to open and parse it if one is found.
        with open(path, "r", encoding="utf-8") as f:
            try:
                return Config(**json.load(f), _path=path)
            except TypeError as exc:
                raise ClickException(
                    f"Invalid {CONFIG_FILENAME} found at {path}") from exc

    def get_path(self) -> Path:
        """Returns the path of the config file."""
        return self._path

    def write(self, path: Optional[Union[Path, str]] = None):
        """Writes the state of this config object to disk.

        Args:
            path: An optional path argument to write the config to, otherwise
                writes to the default _path member stored in the config.
        """
        with open(path if path is not None else self._path, "w",
                  encoding="utf-8") as f:
            # This is added by the @dataclass_json decorator
            # pylint: disable-next=no-member
            f.write(self.json())

    def resolve_asset_paths(self) -> dict[str, Path]:
        """Resolves the relative paths for assets defined in config file."""
        asset_paths = get_field_names(ProjectPaths)
        resolved_asset_paths = {}
        for asset_path in asset_paths:
            try:
                resolved_path = resolve_relative_path(
                    self._path, getattr(self.paths, asset_path))
                resolved_asset_paths[asset_path] = resolved_path
            except Exception as error:
                raise error
        return resolved_asset_paths
