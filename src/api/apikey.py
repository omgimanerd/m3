"""Module to handle getting and setting the API key from the auth file."""

import os
from pathlib import Path
from typing import Optional

from fire.core import FireError

HOME_DIR = Path.home()

M3_FOLDER = '.m3'
AUTH_FILE = 'apikey'


def _get_m3_dir() -> Path:
  path = HOME_DIR / M3_FOLDER
  if not path.exists():
    try:
      os.makedirs(path, mode=0o700)
    except Exception as e:
      raise FireError(f'Unable to create {path}.') from e
  return path


def get_api_key() -> Optional[str]:
  """Gets the CurseForge API key from the credentials file."""
  authfile = _get_m3_dir() / AUTH_FILE
  if not authfile.exists():
    return None
  try:
    with open(authfile, 'r', encoding='utf-8') as f:
      return f.read()
  except Exception as e:
    raise FireError(f'Unable to access {authfile}') from e


def set_api_key(apikey: str):
  """Sets the CurseForge API key from the credentials file."""
  authfile = _get_m3_dir() / AUTH_FILE
  try:
    with open(authfile, 'w+', encoding='utf-8') as f:
      f.write(apikey)
    os.chmod(authfile, 0o600)
  except Exception as e:
    raise FireError(f'Unable to write {authfile}') from e
