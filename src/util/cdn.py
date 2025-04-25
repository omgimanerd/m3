"""Helper functions for downloading files from CDN links."""

import os
from pathlib import Path
from urllib.parse import urlparse

import requests


def _get_filename(url: str) -> str:
    """Extract file name from last part of CDN link.

    Args:
        url: The CDN link to extract file name from

    Returns:
        The last part of the CDN link, to be used as the file name, or an empty 
        string if the URL is invalid or has no path.
    """
    parsed_url = urlparse(url)
    if not parsed_url.path:
        return ""
    return os.path.basename(parsed_url.path)


def download_file(url: str, dest: str):
    """Download mod file from given CDN link.

    Args:
        url: The CDN link to download mod file from
        dest: The destination path to download to
    """
    response = requests.get(url, timeout=10)
    filename = _get_filename(url)
    path = Path(dest) / filename

    with open(path, 'wb') as f:
        f.write(response.content)
