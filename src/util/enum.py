'''Enums used by this codebase.'''

from enum import Enum

class Platform(Enum):
  '''CurseForge or Modrinth, we only support exporting packs to these two
  platforms.'''
  CURSEFORGE = 1
  MODRINTH = 2
