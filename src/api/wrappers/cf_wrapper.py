"""A wrapper class for the CurseForge API."""

from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Callable
from urllib.parse import urljoin

import requests
from click import ClickException

from src.api.dataclasses.cf_response_objects import (CFFile,
                                                     CFGetFilesResponse,
                                                     CFGetModResponse,
                                                     CFGetModsResponse, CFMod)

CF_BASE_URL = 'https://api.curseforge.com'
CF_API_VERSION = 'v1'


class CurseForgeWrapper:  # pylint: disable=too-few-public-methods
    """Wrapper for the CurseForge API."""

    def __init__(self, api_key):
        self.api_key = api_key

    def _get_headers(self) -> dict:
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

    def _get_request(self, path: Path, body: dict = None) -> dict:
        try:
            url = urljoin(CF_BASE_URL, str(Path(CF_API_VERSION) / path))
            response = requests.get(
                url, headers=self._get_headers(), json=body, timeout=10)
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise ClickException(
                'A problem occurred while querying the CurseForge API') from e
        except requests.exceptions.RequestException as e:
            raise ClickException(
                'A problem occurred while querying the CurseForge API') from e
        except JSONDecodeError as e:
            raise ClickException(
                'Failed to decode JSON payload from CurseForge API') from e

    def _post_request(self, path: Path, body: dict = None) -> dict:
        try:
            url = urljoin(CF_BASE_URL, str(Path(CF_API_VERSION) / path))
            response = requests.post(
                url, headers=self._get_headers(), json=body, timeout=10)
            return response.json()
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            raise ClickException(
                'A problem occurred while querying the CurseForge API') from e
        except JSONDecodeError as e:
            raise ClickException(
                'Failed to decode JSON payload from CurseForge API') from e

    def _unpack_request(
            self, path: str, method: str, unpacker: Callable[[object],
                                                             object],
            body: dict = None) -> object:
        try:
            if method == 'GET':
                json = self._get_request(Path(path), body=body)
                return unpacker(json)
            if method == 'POST':
                json = self._post_request(Path(path), body=body)
                return unpacker(json)
        except TypeError as e:
            raise Exception(
                f'Failed to process API response to {path}') from e

    def get_mod(self, mod_id: int) -> CFMod:
        """Return CFGetModData object containing mod metadata.

        Args:
          mod_id: The Mod ID for the mod metadata to be fetched

        Returns:
            An object containing CFGetModResponse object or None, statusCode of
            API request, and status containing status or error message.
        """
        return self._unpack_request(
            f'mods/{mod_id} ', 'GET',
            unpacker=lambda json: CFGetModResponse(**json))

    def get_mods(self, mod_ids: list[int]) -> list[CFMod]:
        """Return list of CFGetModData object containing mod metadata.

        Args:
            mod_ids: List of mod IDs to query

        Returns:
            List of CFGetModResponse objects.
        """
        return self._unpack_request(
            'mods', 'POST',
            body={
                "modIds": mod_ids,
                "filterPcOnly": True
            },
            unpacker=lambda json: CFGetModsResponse(**json))

    def get_asset_files(self, file_ids: list[int]) -> list[CFFile]:
        """Return list of CFFile objects containing file metadata.

        Args:
            file_ids: List of file IDs to query

        Returns:
            A list of CFFile objects.
        """
        return self._unpack_request(
            'mods/files', 'POST',
            body={
                "fileIds": file_ids,
            },
            unpacker=lambda json: CFGetFilesResponse(**json)).data

    def get_asset_file(self, file_id) -> CFFile:
        """Return a CFFile object containing file metadata.

        Args:
            file_id: The CurseForge file ID to query

        Returns:
            A CFFile object.
        """
        return self.get_asset_files([file_id])[0]
