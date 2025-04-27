"""Helper functions for downloading files from CDN links."""

from pathlib import Path

import requests


def download_file(url: str, dest: Path):
    """Download asset file from given CDN link.

    Args:
        url: The CDN link to download asset file from
        dest: The destination path to download to
    """
    response = requests.get(url, timeout=10)
    path = Path(dest)

    with open(path, 'wb+') as f:
        f.write(response.content)
