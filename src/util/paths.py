"""Utility file with path manipulation functions."""

import os
from pathlib import Path
from typing import Optional


def walk_up_search(filename: str) -> Optional[Path]:
  """Walks up from the current execution context looking for a given
  filename.

  Args:
    filename: the filename to search for in parent directories.

  Returns:
    The path to the file, if found, or None.
  """
  current = Path(os.getcwd())
  while True:
    if str(current) == current.root:
      return None
    filepath = current / filename
    if filepath.exists():
      return filepath
    current = current.parent
