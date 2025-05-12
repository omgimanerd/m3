"""Classes for defining assets managed by m3."""


from typing import Union

from src.util.enum import AssetType, Platform, Side


class Asset:
    def __init__(self, name: str, platform: Platform, asset_type: AssetType,
                 side: Side, cdn_link: str):
        self.name = name
        self.platform = platform
        self.asset_type = asset_type
        self.side = side

        self.dependencies = []

        self.cdn_link = cdn_link

    def get_asset_identifier(self) -> tuple[Union[str, int], Union[str, int]]:
        raise NotImplementedError('Subclass should implement this method')


class CurseForgeAsset(Asset):
    """Class wrapper for handling CurseForge lockfile entries."""

    def __init__(
            self, name: str, asset_type: AssetType, side: Side, cdn_link: str,
            project_id: int, file_id: int):
        """
        Args:
            name: A human-readable name for the asset
            asset_type: Mod, resource pack, texture pack, or shader pack etc.
            side: Client, server, or both
            cdn_link: The link to download the asset from
            project_id: The unique identifier for the CurseForge project
            file_id: The unique identifier for the CurseForge asset file
        """
        super().__init__(name, Platform.CURSEFORGE, asset_type, side, cdn_link)
        self.project_id = project_id
        self.file_id = file_id

    def get_asset_identifier(self) -> tuple[Union[str, int], Union[str, int]]:
        return (self.project_id, self.file_id)


class ModrinthAsset(Asset):
    """Class wrapper for handling Modrinth lockfile entries."""

    def __init__(
            self, name: str, asset_type: AssetType, side: Side, cdn_link: str,
            slug: Union[int, str], hash_: str):
        """
        Args:
            name: A human-readable name for the asset
            asset_type: Mod, resource pack, texture pack, or shader pack etc.
            side: Client, server, or both
            cdn_link: The link to download the asset from
            slug: The unique identifier for the Modrinth project
            hash_: The hash of the Modrinth asset file
        """
        super().__init__(name, Platform.CURSEFORGE, asset_type, side, cdn_link)
        self.slug = slug
        self.hash = hash_

    def get_asset_identifier(self) -> tuple[Union[str, int], str]:
        return (self.slug, self.hash)
