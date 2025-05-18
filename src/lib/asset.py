"""Classes for defining assets managed by m3."""


from typing import Self, Union

from pydantic.dataclasses import dataclass

from src.lib.dataclasses import dataclass_json
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
        project_id: The ID used to identify the project on CurseForge
        file_id: The ID used to identify the asset file on CurseForge
    """
    project_id: int
    file_id: int

    def __post_init__(self):
        self.platform = Platform.CURSEFORGE

    def get_asset_identifier(self) -> tuple[Union[str, int], Union[str, int]]:
        return (self.project_id, self.file_id)


@dataclass_json
@dataclass
class ModrinthAsset(Asset):
    """Class wrapper for handling Modrinth lockfile entries.

    Attributes:
        slug: The unique name or ID used to identify the asset on Modrinth
        hash_: The hash of the asset file
    """
    slug: Union[int, str]
    hash_: str

    def __post_init__(self):
        self.platform = Platform.MODRINTH

    def get_asset_identifier(self) -> tuple[Union[str, int], str]:
        return (self.slug, self.hash_)
