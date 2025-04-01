''''''

from dataclasses import dataclass

@dataclass
class LockfileEntries:
  '''Dataclass wrapper for handling lockfile entries.'''
  name: str
  hash: str
