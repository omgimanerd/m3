#!/usr/bin/env python3
'''CLI entry point.'''

import fire


from src.cli.auth import Auth
from src.cli.list import List
from src.cli.init import Init


class M3:
  '''Entry point to m3 CLI'''

  def __init__(self):
    self.auth = Auth()
    self.list = List()
    self.init = Init()


if __name__ == '__main__':
  fire.core.Display = lambda lines, out: print(*lines, file=out)
  fire.Fire(M3)
