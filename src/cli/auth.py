"""auth subcommand module"""

from getpass import getpass

from click import confirm
from fire.core import FireError

from src.api.apikey import get_api_key, set_api_key


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Auth:

    def set(self):
        """Set the CurseForge API key."""
        apikey = getpass(prompt='API Key (will not be displayed): ')
        if not apikey:
            raise FireError('Cannot set empty API key.')
        set_api_key(apikey=apikey)
        print('CurseForge API key set successfully.')

    def show(self):
        """Show the stored CurseForge API key."""
        apikey = get_api_key()
        if apikey is None:
            print('No API key set.')
            return
        if not confirm('Are you sure you want to show the API key?', default=False):
            return
        print(apikey)
