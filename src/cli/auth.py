"""auth subcommand module"""

from src.api.apikey import set_api_key


# pylint: disable-next=too-few-public-methods
class Auth:
  """Sets the CurseForge API key."""

  def set(self, apikey):
    """Set the CurseForge API key."""
    set_api_key(apikey=apikey)
