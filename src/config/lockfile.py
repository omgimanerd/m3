'''Dataclass wrapper for handling m3's lockfile'''

from dataclasses import dataclass

@dataclass
class Lockfile:
  '''Dataclass wrapper for handling m3's lockfile'''
  lockfileentries = None

  def __init__(self):
    pass
