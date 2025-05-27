"""Unit testing for hash.py"""


from src.config.lockfile import HASH_ALGS
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
    assert multikey_dict.len() == 3

    multikey_dict_keys = multikey_dict.get_multikeys()
    assert (
        "a.jar",
        ref_hashes['md5']['a.jar'],
        ref_hashes['sha1']['a.jar'],
        ref_hashes['sha512']['a.jar'],

    ) in multikey_dict_keys

    assert (
        "b.jar",
        ref_hashes['md5']['b.jar'],
        ref_hashes['sha1']['b.jar'],
        ref_hashes['sha512']['b.jar'],
    ) in multikey_dict_keys

    assert (
        "c.zip",
        ref_hashes['md5']['c.zip'],
        ref_hashes['sha1']['c.zip'],
        ref_hashes['sha512']['c.zip'],
    ) in multikey_dict_keys

    assert multikey_dict.get("a.jar") == asset_path / "a.jar"
    assert multikey_dict.get("b.jar") == asset_path / "b.jar"
    assert multikey_dict.get("c.zip") == asset_path / "c.zip"
