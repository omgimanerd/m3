"""A wrapper class for the CurseForge API."""

from json.decoder import JSONDecodeError
from pathlib import Path
from urllib.parse import urljoin

import requests
from fire.core import FireError

from src.api.dataclasses.cf_response_objects import (CFDataResponse,
                                                     CFGetModResponse)

CF_BASE_URL = 'https://api.curseforge.com'
CF_API_VERSION = 'v1'


class CurseForgeWrapper:  # pylint: disable=too-few-public-methods
    """Wrapper for the CurseForge API."""

    def __init__(self, api_key):
        self.api_key = api_key

    def get_mod(self, mod_id: int) -> CFDataResponse:
        """Return CFGetModData object containing mod metadata.

        Parameters:
          mod_id (int): The Mod ID for the mod metadata to be fetched

        Returns:
          CFGetModData:
            Object containing CFGetModResponse object or None, statusCode of API request,
            and status containing status or error message.
        """

        try:
            get_mod_endpoint = 'mods'
            request_path = Path(CF_API_VERSION).joinpath(
                get_mod_endpoint, str(mod_id))
            request_url = urljoin(CF_BASE_URL, str(request_path))

            headers = {
                'Accept': 'application/json',
                'x-api-key': self.api_key
            }

            response = requests.get(request_url, headers=headers, timeout=10)
            mod_data = CFGetModResponse(**response.json())
        except requests.exceptions.HTTPError as err:
            raise FireError(
                f'A problem occurred while querying the CurseForge API for mod {mod_id}') from err
        except requests.exceptions.RequestException as err:
            raise FireError(
                f'A problem occurred while querying the CurseForge API for mod {mod_id}') from err
        except JSONDecodeError as err:
            raise FireError(
                f'Failed to decode JSON payload for mod {mod_id}') from err
        except TypeError as err:
            raise FireError(
                f'Failed to process API response for mod {mod_id}') from err

        return CFDataResponse(
            payload=mod_data, status_code=response.status_code, status=response.reason)
