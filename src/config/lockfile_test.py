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


# def test_lockfile_read(lockfile_from_path):
#     """Tests reading a lockfile from disk."""
#     l = lockfile_from_path("testdata/test_m3.lock.json")
#     assert l == Lockfile(
#         entries={
#             "test-entry": LockfileEntry(
#                 name="test-entry",
#                 hash=HashEntry(
#                     sha1="sha1-hash",
#                     sha512="sha512-hash",
#                     md5="md5-hash"
#                 ),
#                 platform=Platform.CURSEFORGE,
#                 asset_type=AssetType.MOD,
#                 asset=Asset(
#                     name="test-mod",
#                     platform=Platform.CURSEFORGE,
#                     asset_type=AssetType.MOD,
#                     side=Side.BOTH,
#                     dependencies=[
#                         Asset(
#                             name="test-resource-pack",
#                             platform=Platform.CURSEFORGE,
#                             asset_type=AssetType.RESOURCE_PACK,
#                             side=Side.BOTH,
#                             dependencies=[],
#                             cdn_link="test-cdn-link-resource-pack"
#                         )
#                     ],
#                     cdn_link="test-cdn-link"
#                 )
#             )
#         }
#     )


def test_lockfile_serialize_deserialize(lockfile_from_path, tmp_path):
    """Tests that writing a file to disk and reading that file results in the 
    same lockfile object."""
    lockfile_path = tmp_path / LOCKFILE_FILENAME
    l = Lockfile(
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
    l.write()
    written_l = lockfile_from_path(lockfile_path)
    assert l == written_l


def test_lockfile_write():
    """Tests writing a lockfile to disk."""
    pass
