"""Helper functions for web request related tasks."""

from pathlib import Path

import requests


def download_file(url: str, dest: Path):
    """Download asset file from given URL.

    Args:
        url: The URL to download asset file from
        dest: The destination path to download to
    """
    response = requests.get(url, timeout=10)
    path = Path(dest)

    with open(path, 'wb+') as f:
        f.write(response.content)
