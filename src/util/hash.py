"""Utility file with hashing functions."""

import hashlib
from pathlib import Path
from typing import Union

from click import ClickException


def hash_file(filename: Union[str, Path], alg: str) -> str:
    """Returns the hash of the given file using the specified hashing algorithm.

    Args:
        filename: The path to the file to hash
        alg: The hashing algorithm to use

    Returns:
        A hash of the given file as a string.
    """
    with open(filename, 'rb') as f:
        digest = hashlib.file_digest(f, alg)
    return digest.hexdigest()


def hash_jar_dir(dir_: Union[str, Path], alg: str) -> dict[str, str]:
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
    for path in sorted(Path(dir_).iterdir(), key=lambda p: str(p).lower()):
        if path.is_file() and (path.suffix in (".jar", ".zip")):
            file_hash = hash_file(path, alg)
            hashes[file_hash] = path.name

    return hashes


def hash_jar_dir_multi_hash(
        dir_: Union[str, Path], algs: list[str], default_alg: str) -> dict:
    """Returns a dict keyed on the indicated default hashing alg.

    The dict holds a dict with hashes of a .jar file in the given directory 
    along with its file name.

    Args:
        dir_: The directory to search for .jar files to hash
        algs: The hashing algorithms to use when generating hashes for the file
        default_alg: the hashing alg to use when generating the hash to key on

    Returns:
        A dict keyed on the hash of a .jar file using the default alg, 
        containing a dict with the file name and all the hashes generated for a 
        given file.
    """
    if default_alg not in algs:
        raise ClickException('Default hashing alg must be included in alg list')
    hashes = {}
    for path in sorted(Path(dir_).iterdir(), key=lambda p: str(p).lower()):
        if path.is_file() and (path.suffix in (".jar", ".zip")):
            file_data = {}
            for hash_ in algs:
                file_hash = hash_file(path, hash_)
                file_data[hash_] = file_hash
            file_data['file_name'] = path.name
            hashes[file_data[default_alg]] = file_data
    return hashes
