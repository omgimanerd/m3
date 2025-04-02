'''Handles loading m3's config and lockfile.'''

from typing import Optional

from src.config.config import Config
from src.config.lockfile import Lockfile


def load_config_and_lockfile() -> tuple[Optional[Config], Optional[Lockfile]]:
  '''Attempts to load the config and lockfile, surfacing any errors to
  Fire.

  Returns:
    a two-tuple containing the config and lockfile, or Nones if not found
  '''
  config = Config.get_config()
  if config is None:
    return tuple(None, None)
  lockfile = Lockfile.create(config.get_path().parent)
  return tuple(config, lockfile)
