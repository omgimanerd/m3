'''Dataclass wrapper for handling overrides to the default paths'''

from dataclasses import dataclass
from pathlib import Path

@dataclass
class ProjectPaths:
  '''Dataclass for representing paths to '''
  mods: Path = Path('mods')
  resourcepacks: Path = Path('resourcepacks')
  texturepacks: Path = Path('texturepacks')
  shaderpacks: Path = Path('shaderpacks')
