"""Class for defining m3's lockfile entries."""

from pydantic.dataclasses import dataclass

from src.lib.asset import Asset
from src.lib.dataclasses import dataclass_json
from src.util.enum import AssetType, HashAlg, Platform


@dataclass_json
@dataclass
class HashEntry:
    """Dataclass wrapper for handling file hashes of different hash algorithms."""
    sha1: str
    sha512: str
    md5: str

    def __getitem__(self, name: HashAlg):
        if isinstance(name, HashAlg):
            return getattr(self, name.value)
        raise TypeError(
            f'Expected HashAlg for HashEntry attribute, got {type(name)}')


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
