#!/usr/bin/env python3
"""CLI entry point."""

import click

from src.cli.add import add
from src.cli.auth import auth
from src.cli.init import init
from src.cli.list import list_mods
from src.config.config import Config


def test():
    c = Config.get_config()
    print(c)


@click.group()
def m3():
    """Click command group for all m3 commands."""


m3.add_command(init)
m3.add_command(add)
m3.add_command(auth)
m3.add_command(list_mods)


if __name__ == '__main__':
    m3()
