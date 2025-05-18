"""Unit testing for lockfile.py"""

import json

from src.config.lockfile import LOCKFILE_FILENAME, Lockfile
from src.config.lockfile_entry import HashEntry, LockfileEntry
from src.lib.asset import Asset
from src.util.enum import AssetType, Platform, Side


def test_lockfile_creation():
    """Tests that creating an empty lockfile results in a valid lockfile."""
    l = Lockfile()
    assert l == Lockfile(
        entries={}
    )


def test_lockfile_read(lockfile_from_path):
    """Tests reading a lockfile from disk."""
    l = lockfile_from_path("testdata/test_m3.lock.json")
    assert l == Lockfile(
        entries={
            "test-entry": LockfileEntry(
                name="test-entry",
                hash=HashEntry(
                    sha1="sha1-hash",
                    sha512="sha512-hash",
                    md5="md5-hash"
                ),
                platform=Platform.CURSEFORGE,
                asset_type=AssetType.MOD,
                asset=Asset(
                    name="test-mod",
                    platform=Platform.CURSEFORGE,
                    asset_type=AssetType.MOD,
                    side=Side.BOTH,
                    dependencies=[
                        Asset(
                            name="test-resource-pack",
                            platform=Platform.CURSEFORGE,
                            asset_type=AssetType.RESOURCE_PACK,
                            side=Side.BOTH,
                            dependencies=[],
                            cdn_link="test-cdn-link-resource-pack"
                        )
                    ],
                    cdn_link="test-cdn-link"
                )
            )
        },
        _path=l.get_path()
    )


def test_lockfile_write_read(lockfile_from_path, tmp_path):
    """Tests that writing a file to disk and reading that file results in the
    same lockfile object."""
    lockfile_path = tmp_path / LOCKFILE_FILENAME
    lockfile = Lockfile(
        entries={
            "test-entry": LockfileEntry(
                name="test-entry",
                hash=HashEntry(
                    sha1="sha1-hash",
                    sha512="sha512-hash",
                    md5="md5-hash"
                ),
                platform=Platform.CURSEFORGE,
                asset_type=AssetType.MOD,
                asset=Asset(
                    name="test-mod",
                    platform=Platform.CURSEFORGE,
                    asset_type=AssetType.MOD,
                    side=Side.BOTH,
                    dependencies=[
                        Asset(
                            name="test-resource-pack",
                            platform=Platform.CURSEFORGE,
                            asset_type=AssetType.RESOURCE_PACK,
                            side=Side.BOTH,
                            dependencies=[],
                            cdn_link="test-cdn-link-resource-pack"
                        )
                    ],
                    cdn_link="test-cdn-link"
                )
            )
        },
        _path=lockfile_path
    )
    lockfile.write()
    with open(lockfile_path, 'r', encoding='utf-8') as f:
        written_json = json.load(f)

    assert written_json == {
        "entries": {
            "test-entry": {
                "name": "test-entry",
                "hash": {
                    "sha1": "sha1-hash",
                    "sha512": "sha512-hash",
                    "md5": "md5-hash"
                },
                "platform": "curseforge",
                "asset_type": "mod",
                "asset": {
                    "name": "test-mod",
                    "platform": "curseforge",
                    "asset_type": "mod",
                    "side": "both",
                    "dependencies": [
                        {
                            "name": "test-resource-pack",
                            "platform": "curseforge",
                            "asset_type": "resource_pack",
                            "side": "both",
                            "dependencies": [],
                            "cdn_link": "test-cdn-link-resource-pack"
                        }
                    ],
                    "cdn_link": "test-cdn-link"
                }
            }
        }
    }

    # Check that reading back the same lockfile results in the same object
    written_lockfile = lockfile_from_path(lockfile_path)
    assert lockfile == written_lockfile
