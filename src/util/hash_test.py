"""Unit testing for hash.py"""


from src.config.lockfile import HASH_ALGS
from src.util.hash import hash_asset_dir, hash_asset_dir_multi_hash


def test_hash_asset_dir(current_dir, read_json_file):
    """Tests that a directory containing asset files is properly hashed and 
    returned as a dict."""
    ref_hashes = read_json_file(
        current_dir / 'testdata/test_hashes_to_filename.json')
    sha1_hashes = hash_asset_dir(current_dir / 'testdata/assets', 'sha1')
    sha512_hashes = hash_asset_dir(current_dir / 'testdata/assets', 'sha512')
    md5_hashes = hash_asset_dir(current_dir / 'testdata/assets', 'md5')

    assert sha1_hashes == ref_hashes['sha1']
    assert sha512_hashes == ref_hashes['sha512']
    assert md5_hashes == ref_hashes['md5']


def test_hash_asset_dir_multi_hash(current_dir, read_json_file):
    """Tests that a directory containing asset files is properly hashed and 
    returned as a multikey dict."""
    asset_path = current_dir / 'testdata/assets'
    ref_hashes = read_json_file(
        current_dir / 'testdata/test_filename_to_hashes.json')
    multikey_dict = hash_asset_dir_multi_hash(asset_path, HASH_ALGS)
    assert multikey_dict.len() == 4

    multikey_dict_keys = multikey_dict.get_multikeys()
    assert (
        "a.jar", ref_hashes['sha1']['a.jar'],
        ref_hashes['sha512']['a.jar'],
        ref_hashes['md5']['a.jar']
    ) in multikey_dict_keys

    assert (
        "b.jar", ref_hashes['sha1']['b.jar'],
        ref_hashes['sha512']['b.jar'],
        ref_hashes['md5']['b.jar']
    ) in multikey_dict_keys

    assert (
        "c.zip", ref_hashes['sha1']['c.zip'],
        ref_hashes['sha512']['c.zip'],
        ref_hashes['md5']['c.zip']
    ) in multikey_dict_keys

    assert (
        "d.jar", ref_hashes['sha1']['d.jar'],
        ref_hashes['sha512']['d.jar'],
        ref_hashes['md5']['d.jar']
    ) in multikey_dict_keys

    assert multikey_dict.get("a.jar") == asset_path / "mods/a.jar"
    assert multikey_dict.get("b.jar") == asset_path / "mods/b.jar"
    assert multikey_dict.get("c.zip") == asset_path / "mods/c.zip"
    assert multikey_dict.get("d.jar") == asset_path / "texturepacks/d.jar"
