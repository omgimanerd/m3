"""Classes for defining assets managed by m3."""


from typing import Union

from packaging.version import Version
from pydantic.dataclasses import dataclass

from src.api.dataclasses.cf_response_objects import CFFile, CFMod
from src.lib.dataclasses import dataclass_json
from src.util.asset_analysis import (is_older_than_version,
                                     keyword_in_category_url,
                                     keyword_in_modules)
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
        cdn_link: The link to download the asset from
        dependencies: A list of assets this asset depends on
    """
    name: str
    platform: Platform
    asset_type: AssetType
    side: Side
    cdn_link: str
    dependencies: list[str]

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

    @staticmethod
    def identify_cf_asset_type(
            proj_data: CFMod, asset_data: CFFile) -> AssetType:
        """Attempts to identify the asset type for a given asset file using
        project and asset data from the CurseForge API.

        Args:
            proj_data: The project data for this asset
            asset_data: The data for this specific asset file

        Returns:
            The AssetType for the given asset file or raises a ValueError if 
            unable to determine the asset type with the given data.
        """
        if keyword_in_category_url(proj_data.categories, "/mc-mods/"):
            return AssetType.MOD
        if keyword_in_category_url(proj_data.categories, "/shaders/"):
            return AssetType.SHADER_PACK
        if not is_older_than_version(asset_data.gameVersions, Version("1.6.1")):
            return AssetType.RESOURCE_PACK
        if keyword_in_modules(asset_data.modules, "pack.mcmeta"):
            return AssetType.RESOURCE_PACK
        if keyword_in_modules(asset_data.modules, ".png"):
            return AssetType.TEXTURE_PACK
        raise ValueError(
            f'Unable to identify asset type for {asset_data.displayName}, ' +
            'skipping...')


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
