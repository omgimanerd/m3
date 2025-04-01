import requests

from src.api.dataclasses.cf_response_objects import CFGetModResponse, CFGetModData


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

        response = requests.get(get_mod_url, headers=headers)
        mod_data = CFGetModResponse(**response.json())

        return mod_data.data
