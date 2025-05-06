"""auth subcommand module"""

from getpass import getpass

import click
from fire.core import FireError

from src.api.apikey import get_api_key, set_api_key
from src.util.click_helpers import CONTEXT_SETTINGS


# pylint: disable-next=missing-class-docstring
class Auth:
    # TODO: Modify help display so subcommands of auth show at same level
    # as subcommands like init and add
    @click.group()
    @staticmethod
    def auth():
        """Command subgroup for auth subcommands."""

    @click.command(context_settings=CONTEXT_SETTINGS)
    @staticmethod
    def set():
        """Sets the CurseForge API key."""
        apikey = getpass(prompt='API Key (will not be displayed): ')
        if not apikey:
            raise FireError('Cannot set empty API key.')
        set_api_key(apikey=apikey)
        print('CurseForge API key set successfully.')

    @click.command(context_settings=CONTEXT_SETTINGS)
    @staticmethod
    def show():
        """Shows the currently stored CurseForge API key."""
        apikey = get_api_key()
        if apikey is None:
            print('No API key set.')
            return
        if not click.confirm('Are you sure you want to show the API key?', default=False):
            return
        print(apikey)

    auth.add_command(set)
    auth.add_command(show)
