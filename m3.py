#!/usr/bin/env python3
'''CLI entry point.'''

from src.cli.auth import Auth
from src.cli.config import Config_

import fire

class M3(object):
  '''Entry point to m3 command line application'''

  def __init__(self):
    self.auth = Auth()
    self.export = Auth()
    self.config = Config_.create()

if __name__ == '__main__':
  fire.Fire(M3)
