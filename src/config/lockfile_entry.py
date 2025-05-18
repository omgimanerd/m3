"""Class for defining m3's lockfile entries."""

from pydantic.dataclasses import dataclass

from src.lib.asset import Asset
from src.lib.dataclasses import dataclass_json
from src.util.enum import AssetType, Platform


@dataclass_json
@dataclass
class HashEntry:
    """Dataclass wrapper for handling file hashes of different hash algorithms."""
    sha1: str
    sha512: str
    md5: str


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
