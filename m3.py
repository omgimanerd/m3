#!/usr/bin/env python3
'''CLI entry point.'''

import fire

from src.cli.auth import Auth
from src.cli.list import List
from src.cli.init import Init
from src.config.config import Config

from src.util.exceptions import M3Exception

class M3:
  '''Entry point to m3 CLI'''

  def __init__(self):
    try:
      self._config = Config.get_config()
    except M3Exception as e:
      print(e.args[0])
      return
    self._lockfile = None

    self.auth = Auth()
    self.list = List()
    self.init = Init()

if __name__ == '__main__':
  fire.core.Display = lambda lines, out: print(*lines, file=out)
  fire.Fire(M3)
