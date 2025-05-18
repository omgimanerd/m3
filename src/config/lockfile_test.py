"""Unit testing for lockfile.py"""

import json

import pytest

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
        }
    )


@pytest.mark.only
def test_lockfile_serialize_deserialize(lockfile_from_path, tmp_path):
    """Tests that writing a file to disk and reading that file results in the
    same lockfile object."""
    lockfile_path = tmp_path / LOCKFILE_FILENAME
    # l = Lockfile(
    #     entries={
    #         "test-entry": LockfileEntry(
    #             name="test-entry",
    #             hash=HashEntry(
    #                 sha1="sha1-hash",
    #                 sha512="sha512-hash",
    #                 md5="md5-hash"
    #             ),
    #             platform=Platform.CURSEFORGE,
    #             asset_type=AssetType.MOD,
    #             asset=Asset(
    #                 name="test-mod",
    #                 platform=Platform.CURSEFORGE,
    #                 asset_type=AssetType.MOD,
    #                 side=Side.BOTH,
    #                 dependencies=[
    #                     Asset(
    #                         name="test-resource-pack",
    #                         platform=Platform.CURSEFORGE,
    #                         asset_type=AssetType.RESOURCE_PACK,
    #                         side=Side.BOTH,
    #                         dependencies=[],
    #                         cdn_link="test-cdn-link-resource-pack"
    #                     )
    #                 ],
    #                 cdn_link="test-cdn-link"
    #             )
    #         )
    #     },
    #     _path=lockfile_path
    # )
    le = LockfileEntry(
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
    l = Lockfile(entries={"test-entry": le},  _path=lockfile_path)
    l.write()
    written_l = lockfile_from_path(lockfile_path)
    print(written_l)
    print(l)
    print(le)
    assert l == written_l


def test_lockfile_entry_serializable(tmp_path, lockfile_entry_from_path):
    lockfile_path = tmp_path / LOCKFILE_FILENAME
    l = LockfileEntry(
        name="test",
        hash=HashEntry(sha1="sha1", sha512="sha512", md5="md5"),
        platform=Platform.CURSEFORGE,
        asset_type=AssetType.MOD,
        asset=Asset(
            name="test_asset",
            platform=Platform.CURSEFORGE,
            asset_type=AssetType.MOD,
            side=Side.BOTH,
            cdn_link="link",
            dependencies=[]
        )
    )
    with open(lockfile_path, 'w', encoding='utf-8') as f:
        f.write(l.json())

    written_l = lockfile_entry_from_path(lockfile_path)
    print(written_l)


def test_hash_entry_serializable(tmp_path):
    lockfile_path = tmp_path / LOCKFILE_FILENAME
    h = HashEntry(
        sha1="sha1",
        sha512="sha512",
        md5="md5"
    )
    with open(lockfile_path, 'w', encoding='utf-8') as f:
        f.write(h.json())


def test_lockfile_write():
    """Tests writing a lockfile to disk."""
    pass
