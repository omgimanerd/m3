"""Unit testing for lockfile.py"""

import json

from src.config.lockfile import LOCKFILE_FILENAME, Lockfile
from src.config.lockfile_entry import HashEntry, LockfileEntry
from src.lib.asset import Asset
from src.util.enum import AssetType, Platform, Side


def test_lockfile_creation():
    """Tests that creating an empty lockfile results in a valid lockfile."""
    # We do not have to assert that _path matches because it defaults to the
    # same value
    l = Lockfile()
    assert l == Lockfile(
        entries={}
    )


def test_lockfile_read_write(
        lockfile_from_path, current_dir, tmp_path, read_file):
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
                        "test-texture-pack"
                    ],
                    cdn_link="test-cdn-link"
                )
            ),
            "test-texture-pack": LockfileEntry(
                name="test-texture-pack",
                hash=HashEntry(
                    sha1="sha1-hash-texture",
                    sha512="sha512-hash-texture",
                    md5="md5-hash-texture"
                ),
                platform=Platform.CURSEFORGE,
                asset_type=AssetType.TEXTURE_PACK,
                asset=Asset(
                    name="test-texture-pack",
                    platform=Platform.CURSEFORGE,
                    asset_type=AssetType.TEXTURE_PACK,
                    side=Side.BOTH,
                    dependencies=[],
                    cdn_link="test-cdn-link"
                )
            )
        },
        _path=l.get_path()
    )

    # Write the lockfile back to a file and compare the contents.
    output_path = tmp_path / LOCKFILE_FILENAME
    l.write(output_path)
    assert read_file(
        current_dir / "testdata/test_m3.lock.json") == read_file(output_path)


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
                        "test-texture-pack"
                    ],
                    cdn_link="test-cdn-link"
                )
            ),
            "test-texture-pack": LockfileEntry(
                name="test-texture-pack",
                hash=HashEntry(
                    sha1="sha1-hash-texture",
                    sha512="sha512-hash-texture",
                    md5="md5-hash-texture"
                ),
                platform=Platform.CURSEFORGE,
                asset_type=AssetType.TEXTURE_PACK,
                asset=Asset(
                    name="test-texture-pack",
                    platform=Platform.CURSEFORGE,
                    asset_type=AssetType.TEXTURE_PACK,
                    side=Side.BOTH,
                    dependencies=[],
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
                    "cdn_link": "test-cdn-link",
                    "dependencies": [
                        "test-texture-pack"
                    ]
                }
            },
            "test-texture-pack": {
                "name": "test-texture-pack",
                "hash": {
                    "sha1": "sha1-hash-texture",
                    "sha512": "sha512-hash-texture",
                    "md5": "md5-hash-texture"
                },
                "platform": "curseforge",
                "asset_type": "texture_pack",
                "asset": {
                    "name": "test-texture-pack",
                    "platform": "curseforge",
                    "asset_type": "texture_pack",
                    "side": "both",
                    "cdn_link": "test-cdn-link",
                    "dependencies": []
                }
            }
        }
    }

    # Check that reading back the same lockfile results in the same object
    written_lockfile = lockfile_from_path(lockfile_path)
    assert lockfile == written_lockfile


def test_lockfile_multikey_dict_creation(lockfile_from_path):
    """Tests creating a multikey dict from a lockfile object."""
    lockfile = lockfile_from_path("testdata/test_m3.lock.json")
    multikey_dict = lockfile.create_multikey_dict_for_lockfile()
    assert multikey_dict.len() == 2

    multikey_dict_keys = multikey_dict.get_multikeys()
    assert ("test-entry", "sha1-hash", "sha512-hash",
            "md5-hash") in multikey_dict_keys
    assert ("test-texture-pack", "sha1-hash-texture", "sha512-hash-texture",
            "md5-hash-texture") in multikey_dict_keys
    assert multikey_dict.get("test-entry") == LockfileEntry(
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
                "test-texture-pack"
            ],
            cdn_link="test-cdn-link"
        )
    )
    assert multikey_dict.get("test-texture-pack") == LockfileEntry(
        name="test-texture-pack",
        hash=HashEntry(
            sha1="sha1-hash-texture",
            sha512="sha512-hash-texture",
            md5="md5-hash-texture"
        ),
        platform=Platform.CURSEFORGE,
        asset_type=AssetType.TEXTURE_PACK,
        asset=Asset(
            name="test-texture-pack",
            platform=Platform.CURSEFORGE,
            asset_type=AssetType.TEXTURE_PACK,
            side=Side.BOTH,
            dependencies=[],
            cdn_link="test-cdn-link"
        )
    )
