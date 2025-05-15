"""Class for defining m3's lockfile entries."""

from dataclasses import dataclass, field

from src.lib.asset import Asset
from src.util.enum import AssetType, Platform


@dataclass
class HashEntry:
    """Dataclass wrapper for handling file hashes of different hash algorithms."""
    sha1: str
    sha512: str
    md5: str


@dataclass
class LockfileEntry:
    """Class for defining lockfile entries."""
    name: str
    # TODO: Consider redesigning hash/HashEntry into something simpler
    hash: HashEntry = field(default=HashEntry)
    platform: Platform = field(default=Platform)
    asset_type: AssetType = field(default=AssetType)
    asset: Asset = field(default_factory=Asset)
