import fire
import requests
from json.decoder import JSONDecodeError
from src.api.dataclasses.cf_response_objects import CFGetModResponse, CFGetModData, CFDataResponse


class CurseForgeWrapper:
    """Wrapper for the CurseForge API."""

  def __init__(self, api_key):
    self.api_key = api_key

    def get_mod(self, mod_id: int) -> CFGetModData:
        """
        Return CFGetModData object containing mod metadata

    Parameters:
    mod_id (int): The Mod ID for the mod metadata to be fetched

        Returns:
        CFGetModData: Object containing mod metadata
        """
        get_mod_url = f'https://api.curseforge.com/v1/mods/{mod_id}'
        headers = {
            'Accept': 'application/json',
            'x-api-key': self.api_key
        }

    try:
      response = requests.get(get_mod_url, headers=headers,
                              timeout=10)  # 10 second timeout
    except requests.exceptions.HTTPError as err:
      raise FireError(
        f'A problem occurred while querying the CurseForge API for mod {mod_id}') from err
    except requests.exceptions.RequestException as err:
      raise FireError(
        f'A problem occurred while querying the CurseForge API for mod {mod_id}') from err

    try:
      mod_data = CFGetModResponse(**response.json())
    except JSONDecodeError as err:
      raise FireError(
        f'Failed to decode JSON payload for mod {mod_id}') from err
    except TypeError as err:
      raise FireError(
        f'Failed to process API response for mod {mod_id}') from err

    return CFDataResponse(payload=mod_data, statusCode=response.status_code, status=response.reason)
