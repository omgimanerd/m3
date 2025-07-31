"""Class for defining m3's lockfile entries."""

from typing import Union

from pydantic.dataclasses import dataclass

from src.api.dataclasses.cf_response_objects import CFFile, CFMod
from src.lib.asset import Asset, CurseForgeAsset
from src.lib.dataclasses import dataclass_json
from src.util.enum import AssetType, HashAlg, Platform


@dataclass_json
@dataclass
class HashEntry:
    """Dataclass wrapper for handling file hashes of different hash algorithms."""
    sha1: Union[str, None]
    sha512: Union[str, None]
    md5: Union[str, None]

    def __getitem__(self, name: HashAlg):
        if isinstance(name, HashAlg):
            return getattr(self, name.value)
        raise TypeError(
            f'Expected HashAlg for HashEntry attribute, got {type(name)}')

    @staticmethod
    def create_hash_entry_from_cf_resp_obj(resp_obj: CFFile):
        """Generate a hash entry using the hashes in the response object from
        the CurseForge API."""
        file_hashes = {}
        for hash_ in resp_obj.hashes:
            if hash_.algo == 1:
                file_hashes['sha1'] = hash_.value
            elif hash_.algo == 2:
                file_hashes['md5'] = hash_.value

        return HashEntry(**file_hashes, sha512=None)


@dataclass_json
@dataclass
class LockfileEntry:
    """Class for defining lockfile entries."""
    name: str
    # TODO: Consider redesigning hash/HashEntry into something simpler
    hash: HashEntry
    platform: Platform
    asset_type: AssetType
    asset: Asset

    @staticmethod
    def create_lockfile_entry_from_resp_obj(
            proj_data: CFMod, asset_data: CFFile):
        """Given a response object from the CurseForge API, create a lockfile
        entry.

        Args:
            proj_data: The project data for this asset
            asset_data: The data for this specific asset file

        Returns:
            A lockfile entry object
        """
        # TODO: Have method also accept Modrinth response objects
        try:
            cf_asset = CurseForgeAsset.response_object_to_cf_asset(asset_data)
            asset_hashes = HashEntry.create_hash_entry_from_cf_resp_obj(
                asset_data)
            asset_type = CurseForgeAsset.identify_cf_asset_type(
                proj_data, asset_data)
            return LockfileEntry(
                name=cf_asset.name, hash=asset_hashes,
                platform=Platform.CURSEFORGE, asset_type=asset_type,
                asset=cf_asset)
        except ValueError as error:
            raise Exception(
                'Something went wrong while processing data for ' +
                f'{asset_data.displayName}: {error}') from error
