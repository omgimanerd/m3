"""Classes for defining assets managed by m3."""


from dataclasses import dataclass, field
from typing import Self, Union

from src.lib.json import dataclass_json
from src.util.enum import AssetType, Platform, Side


@dataclass_json
@dataclass
class Asset:
    """Class for handling asset data managed by m3.

    Attributes:
        name: A human-readable name for the asset
        platform: The platform the asset is for (CurseForge, Modrinth, etc.)
        asset_type: Mod, resource pack, texture pack, or shader pack etc.
        side: Client, server, or both
        dependencies: A list of assets this asset depends on
        cdn_link: The link to download the asset from
    """
    name: str
    platform: Platform
    asset_type: AssetType
    side: Side
    dependencies: list[Self]
    cdn_link: str

    # pylint: disable-next=missing-function-docstring
    def get_asset_identifier(self) -> tuple[Union[str, int], Union[str, int]]:
        raise NotImplementedError('Subclass should implement this method')


@dataclass_json
@dataclass
class CurseForgeAsset(Asset):
    """Class wrapper for handling CurseForge lockfile entries.

    Attributes:
        platform: The platform the asset is for (CurseForge)
        project_id: The ID used to identify the project on CurseForge
        file_id: The ID used to identify the asset file on CurseForge
    """
    platform: Platform = field(default=Platform.CURSEFORGE)
    project_id: int
    file_id: int

    def get_asset_identifier(self) -> tuple[Union[str, int], Union[str, int]]:
        return (self.project_id, self.file_id)


@dataclass_json
@dataclass
class ModrinthAsset(Asset):
    """Class wrapper for handling Modrinth lockfile entries.

    Attributes:
        platform: The platform the asset is for (Modrinth)
        slug: The unique name or ID used to identify the asset on Modrinth
        hash_: The hash of the asset file
    """
    platform: Platform = field(default=Platform.MODRINTH)
    slug: Union[int, str]
    hash_: str

    def get_asset_identifier(self) -> tuple[Union[str, int], str]:
        return (self.slug, self.hash_)
