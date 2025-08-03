"""Class for defining m3's lockfile entries."""

import os
from pathlib import Path
from typing import Optional

from pydantic.dataclasses import dataclass

from src.api.dataclasses.cf_response_objects import (CF_HASH_ALG_MAP, CFFile,
                                                     CFMod)
from src.lib.asset import Asset, CurseForgeAsset
from src.lib.dataclasses import dataclass_json
from src.util.enum import AssetType, HashAlg, Platform
from src.util.hash import hash_file


@dataclass_json
@dataclass
class HashEntry:
    """Dataclass wrapper for handling file hashes of different hash algorithms."""
    sha1: Optional[str]
    sha512: Optional[str]
    md5: Optional[str]

    def __getitem__(self, name: HashAlg):
        if isinstance(name, HashAlg):
            return getattr(self, name.value)
        raise TypeError(
            f'Expected HashAlg for HashEntry attribute, got {type(name)}')

    @staticmethod
    def create_hash_entry_from_cf_resp_obj(resp_obj: CFFile) -> 'HashEntry':
        """Generate a hash entry using the hashes in the response object from
        the CurseForge API."""
        file_hashes = {}
        try:
            for hash_ in resp_obj.hashes:
                file_hashes[CF_HASH_ALG_MAP[hash_['algo']]] = hash_['value']
        except KeyError as error:
            raise Exception('Error occurred while processing data for ' +
                            f'{resp_obj.displayName}: {error}') from error

        return HashEntry(**file_hashes, sha512=None)

    def populate_hashes(self, filename: Path):
        """Populates missing HashEntry fields by computing the missing hashes
        for a given file."""
        for alg, hash_ in self.__dict__.items():
            if not hash_:
                missing_alg = HashAlg(alg)
                setattr(self, alg, hash_file(filename, missing_alg.value))

    def check_hash(self, filename: Path) -> bool:
        """Checks if the given file's hash matches a hash on file.

            Args:
                filename: The Path to the file to check

            Returns:
                True if the hash of the file matches, False otherwise. Raises a
                FileNotFoundError if the target file does not exist.
            """
        if os.path.exists(filename):
            for alg, expected_hash in self.__dict__.items():
                if expected_hash:
                    common_alg = HashAlg(alg)
                    actual_hash = hash_file(filename, common_alg.value)
                    return actual_hash == expected_hash
        else:
            raise FileNotFoundError(f'Expected file {filename} not found')
        return False


@dataclass_json
@dataclass
class LockfileEntry:
    """Class for defining lockfile entries."""
    name: str
    display_name: str
    # TODO: Consider redesigning hash/HashEntry into something simpler
    hash: HashEntry
    platform: Platform
    asset_type: AssetType
    asset: Asset

    @staticmethod
    def create_lockfile_entry_from_resp_obj(
            proj_data: CFMod, asset_data: CFFile) -> 'LockfileEntry':
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
            cf_asset = CurseForgeAsset.response_object_to_cf_asset(
                proj_data, asset_data)
            asset_hashes = HashEntry.create_hash_entry_from_cf_resp_obj(
                asset_data)
            return LockfileEntry(
                name=cf_asset.name, display_name=cf_asset.display_name,
                hash=asset_hashes, platform=Platform.CURSEFORGE,
                asset_type=cf_asset.asset_type, asset=cf_asset)
        except ValueError as error:
            raise Exception(
                'Something went wrong while processing data for ' +
                f'{asset_data.displayName}: {error}') from error
