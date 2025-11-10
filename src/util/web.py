"""Helper functions for web request related tasks."""

from pathlib import Path

import requests

from src.config.lockfile_entry import HashEntry
from src.util.hash import hash_response_content


def download_file(url: str, dest: Path, file_hashes: HashEntry):
    """Download asset file from given URL.

    Args:
        url: The URL to download asset file from
        dest: The destination path to download to
    """
    try:
        response = requests.get(url, timeout=10)
        path = Path(dest)
        response.raise_for_status()
        common_alg, expected_hash = file_hashes.get_saved_hash()
        if expected_hash != hash_response_content(response, common_alg):
            raise ValueError(
                "Downloaded file hash and expected hash do not match.")

        with open(path, 'wb+') as f:
            f.write(response.content)
    except requests.HTTPError as error:
        raise error
    except ValueError as error:
        raise error
