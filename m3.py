#!/usr/bin/env python3
"""CLI entry point."""

import click

from src.cli.add import Add
from src.cli.auth import Auth
from src.cli.init import Init
from src.cli.list import List
from src.config.config import Config


def test():
    c = Config.get_config()
    print(c)


@click.group()
def m3():
    """Click command group for all m3 commands."""


m3.add_command(Init.init)
m3.add_command(Add.add)
m3.add_command(Auth.auth)
m3.add_command(List.list)


if __name__ == '__main__':
    m3()
