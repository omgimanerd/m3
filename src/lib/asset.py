"""Classes for defining assets managed by m3."""


import re
from typing import Union

from packaging.version import InvalidVersion, Version
from pydantic.dataclasses import dataclass

from src.api.dataclasses.cf_response_objects import CFFile, CFMod
from src.lib.dataclasses import dataclass_json
from src.util.enum import AssetType, Platform, PlatformSuffix, Side


def is_older_than_version(
        supported: list[str],
        target_version: Version) -> bool:
    """Determines if an asset that supports a list of versions is older than a
    given target version.

    Args:
        supported: The list of versions an asset supports
        target_version: The version to compare the supported versions to

    Returns:
        True if all supported versions are older than the target version, False
        otherwise.
    """
    for v in supported:
        try:
            version = Version(v)
            if version >= target_version:
                return False
        except InvalidVersion:
            continue
    return True


def keyword_in_category_url(categories: list[dict], keyword: str) -> bool:
    """Determines if a keyword exists in the path of at least one of the
    category URLs for the given list of categories.

    Args:
        categories: The list of categories to parse the URLs of
        keyword: The keyword to look for

    Returns:
        True if the keyword is found in at least one of the category URLs, False
        otherwise.
    """
    return any(keyword in category['url'] for category in categories)


def keyword_in_modules(modules: list[dict], keyword: str) -> bool:
    """Determines if a keyword exists in the name of at least one of the given
    modules.

    Args:
        modules: The list of modules to parse the names of
        keyword: The keyword to look for

    Returns:
        True if the keyword is found in the name of at least one of the modules,
        False otherwise
    """
    return any(keyword in module['name'] for module in modules)


def generate_internal_id(display_name: str, platform: Platform) -> str:
    """Generates an internal identifier for m3 to use for an asset given the
    asset's display name and platform.

    Args:
        display_name: The display name of the asset platform: CurseForge or
        Modrinth

    Returns:
        An alphanumeric internal identifier with no spaces or special characters
        in lowercase
    """
    suffix = PlatformSuffix.CURSEFORGE.value if platform == Platform.CURSEFORGE else PlatformSuffix.MODRINTH.value
    filtered = re.sub(r'[^a-zA-Z0-9.\- ]', '', display_name)
    filtered = re.sub(r'[.\-]', ' ', filtered)
    return filtered.strip().lower().replace(' ', '-') + suffix


@dataclass_json
@dataclass
class Asset:
    """Class for handling asset data managed by m3.

    Attributes:
        name: The internal identifier of the asset
        display_name: A human-readable name for the asset
        file_name: The file name of the asset uploaded to the asset Platform
        platform: The platform the asset is for (CurseForge, Modrinth, etc.)
        asset_type: Mod, resource pack, texture pack, or shader pack etc.
        side: Client, server, or both
        cdn_link: The link to download the asset from
        dependencies: A list of assets this asset depends on
    """
    name: str   # internal ID
    display_name: str
    # TODO: Decide what layer(s) file_name should live on
    file_name: str
    platform: Platform
    asset_type: AssetType
    side: Side
    cdn_link: str
    dependencies: list

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

    @staticmethod
    def response_object_to_cf_asset(proj_data: CFMod, asset_data: CFFile):
        """Constructor to convert the given CFFile response object from the
        CurseForge API to a CurseForgeAsset object.

        Args:
            proj_data: The data for the mod
            asset_data: The data for the asset

        Returns:
            A CurseForgeAsset object
        """
        asset_type = CurseForgeAsset.identify_cf_asset_type(
            proj_data, asset_data)
        internal_id = generate_internal_id(
            asset_data.displayName, Platform.CURSEFORGE)
        # pylint: disable-next=no-value-for-parameter
        return CurseForgeAsset(
            name=internal_id, display_name=asset_data.displayName,
            file_name=asset_data.fileName, platform=Platform.CURSEFORGE,
            asset_type=asset_type, side=Side.BOTH
            if asset_data.isServerPack else Side.CLIENT,
            cdn_link=asset_data.downloadUrl,
            dependencies=asset_data.dependencies, project_id=asset_data.modId,
            file_id=asset_data.id)


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
