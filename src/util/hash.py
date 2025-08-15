"""Utility file with hashing functions."""

import hashlib
from pathlib import Path

from src.lib.multikey_dict import MultiKeyDict
from src.util.enum import HashAlg


def hash_file(filename: Path, alg: str) -> str:
    """Returns the hash of the given file using the specified hashing algorithm.

    Args:
        filename: The path to the file to hash
        alg: The hashing algorithm to use

    Returns:
        A hash of the given file as a string.
    """
    with open(filename, 'rb') as f:
        return hashlib.file_digest(f, alg).hexdigest()


def hash_asset_dir(dir_: Path, alg: HashAlg) -> dict[str, str]:
    """Returns a dict containing hashes of all .jar and .zip files in the given
    directory.

    The dict is indexed by the hashes of the files. Each file hash will be keyed
    to a dict that contains that hash and the file name.

    Args:
        dir_: The directory to look for files to hash
        alg: The hashing algorithm to use

    Returns:
        A dict indexed by the file hash containing the file hash and file name.
    """
    hashes = {}
    asset_files = list(dir_.glob('*.jar')) + list(dir_.glob('*.zip'))
    for file in asset_files:
        hashes[hash_file(file, alg.value)] = file.name

    return hashes


def hash_asset_dir_multi_hash(dir_: Path,
                              algs: list[HashAlg]) -> MultiKeyDict:
    """Returns a multikey dict containing the path to the corresponding asset
    file path.

    The multikey consists of the name of the asset and hashes of the asset files
    using the provided list of hashing algorithms. Note that the order of the 
    hashing algorithm matters and must be consistent.

    Args:
        dir_: The directory to search for .jar files to hash algs: The hashing
        algorithms to use when generating hashes for the file

    Returns:
        A multikey dict keyed on the asset name and generated hashes of the
        asset file, containing the path to the asset file.
    """
    multikey_dict = MultiKeyDict(len(algs) + 1)
    asset_files = list(dir_.glob('*.jar')) + list(dir_.glob('*.zip'))
    for path in asset_files:
        keys = [path.name]
        for alg in sorted(algs, key=lambda member: member.value):
            keys.append(hash_file(path, alg.value))
        multikey = tuple(keys)

        multikey_dict.add(multikey, path)

    return multikey_dict
