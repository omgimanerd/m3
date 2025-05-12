"""Class for defining m3's lockfile entries."""

from dataclasses import dataclass

from src.lib.asset import Asset
from src.util.enum import AssetType, Platform


@dataclass
class HashEntry:
    """Dataclass wrapper for handling file hashes of different hash algorithms."""
    sha1: str
    sha512: str
    md5: str


class LockfileEntry:
    """Class for defining lockfile entries."""
    name: str
    hash: HashEntry  # TODO: Consider redesigning this into something simpler
    platform: Platform
    asset_type: AssetType
    asset: Asset
