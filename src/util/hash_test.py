"""Unit testing for hash.py"""


from src.config.lockfile import HASH_ALGS
from src.lib.multikey_dict import MultiKeyDict
from src.util.enum import HashAlg
from src.util.hash import hash_asset_dir, hash_asset_dir_multi_hash


def test_hash_asset_dir(current_dir, read_json_file):
    """Tests that a directory containing asset files is properly hashed and 
    returned as a dict."""
    ref_hashes = read_json_file(
        current_dir / 'testdata/test_hashes_to_filename.json')
    sha1_hashes = hash_asset_dir(current_dir / 'testdata/mods', HashAlg.SHA1)
    sha512_hashes = hash_asset_dir(
        current_dir / 'testdata/mods', HashAlg.SHA512)
    md5_hashes = hash_asset_dir(current_dir / 'testdata/mods', HashAlg.MD5)

    assert sha1_hashes == ref_hashes['sha1']
    assert sha512_hashes == ref_hashes['sha512']
    assert md5_hashes == ref_hashes['md5']


def test_hash_asset_dir_multi_hash(current_dir, read_json_file):
    """Tests that a directory containing asset files is properly hashed and 
    returned as a multikey dict."""
    asset_path = current_dir / 'testdata/mods'
    ref_hashes = read_json_file(
        current_dir / 'testdata/test_filename_to_hashes.json')
    multikey_dict = hash_asset_dir_multi_hash(asset_path, HASH_ALGS)
    ref_dict = MultiKeyDict(4)
    ref_dict.add((
        "a.jar",
        ref_hashes['md5']['a.jar'],
        ref_hashes['sha1']['a.jar'],
        ref_hashes['sha512']['a.jar'],

    ), asset_path / "a.jar")
    ref_dict.add((
        "b.jar",
        ref_hashes['md5']['b.jar'],
        ref_hashes['sha1']['b.jar'],
        ref_hashes['sha512']['b.jar'],
    ), asset_path / "b.jar")
    ref_dict.add((
        "c.zip",
        ref_hashes['md5']['c.zip'],
        ref_hashes['sha1']['c.zip'],
        ref_hashes['sha512']['c.zip'],
    ), asset_path / "c.zip")

    assert multikey_dict == ref_dict
